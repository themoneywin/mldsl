const vscode = require("vscode");
const fs = require("fs");
const path = require("path");
const cp = require("child_process");

const output = vscode.window.createOutputChannel("MLDSL Helper");
let seq = 0;

function readJsonSafe(p) {
  try {
    if (!p) return null;
    if (!fs.existsSync(p)) return null;
    return JSON.parse(fs.readFileSync(p, "utf8"));
  } catch {
    return null;
  }
}

function getConfig() {
  const cfg = vscode.workspace.getConfiguration("mldsl");
  return {
    apiAliasesPath: cfg.get("apiAliasesPath"),
    docsRoot: cfg.get("docsRoot"),
    pythonPath: cfg.get("pythonPath"),
    compilerPath: cfg.get("compilerPath"),
    planPath: cfg.get("planPath"),
  };
}

function loadApi() {
  const { apiAliasesPath } = getConfig();
  return readJsonSafe(apiAliasesPath) || {};
}

function buildLookup(api) {
  const lookup = {};
  for (const [moduleName, funcs] of Object.entries(api)) {
    lookup[moduleName] = { byName: {}, canonical: funcs };
    for (const [funcName, spec] of Object.entries(funcs)) {
      lookup[moduleName].byName[funcName] = { funcName, spec };
      const aliases = Array.isArray(spec.aliases) ? spec.aliases : [];
      for (const a of aliases) {
        if (!a) continue;
        lookup[moduleName].byName[a] = { funcName, spec };
      }
    }
  }
  // hardcoded module aliases (draft)
  if (lookup.player && !lookup["игрок"]) lookup["игрок"] = lookup.player;
  if (lookup.event && !lookup["событие"]) lookup["событие"] = lookup.event;
  return lookup;
}

function findModuleAndPrefix(lineText, positionChar) {
  const left = lineText.slice(0, positionChar);
  const re = /([a-zA-Z_\u0400-\u04FF][\w\u0400-\u04FF]*)\.([\w\u0400-\u04FF]*)/g;
  let m;
  let last = null;
  while ((m = re.exec(left))) {
    last = { module: m[1], prefix: m[2] || "", end: m.index + m[0].length };
  }
  if (!last) return null;
  // only trigger when cursor is right after the match
  if (last.end !== left.length) return null;
  return { module: last.module, prefix: last.prefix };
}

function findQualifiedAtPosition(document, position) {
  const line = document.lineAt(position.line).text;
  const re = /([a-zA-Z_\u0400-\u04FF][\w\u0400-\u04FF]*)\.([\w\u0400-\u04FF]+)/g;
  let m;
  while ((m = re.exec(line))) {
    const start = m.index;
    const end = m.index + m[0].length;
    if (position.character >= start && position.character <= end) {
      const range = new vscode.Range(
        new vscode.Position(position.line, start),
        new vscode.Position(position.line, end)
      );
      return { module: m[1], func: m[2], range, text: m[0] };
    }
  }
  return null;
}

function specToMarkdown(spec) {
  function escapeHtml(s) {
    return (s || "")
      .replace(/&/g, "&amp;")
      .replace(/</g, "&lt;")
      .replace(/>/g, "&gt;")
      .replace(/\"/g, "&quot;");
  }

  function mcToHtml(s) {
    if (!s) return "";
    const colors = {
      "0": "#000000",
      "1": "#0000AA",
      "2": "#00AA00",
      "3": "#00AAAA",
      "4": "#AA0000",
      "5": "#AA00AA",
      "6": "#FFAA00",
      "7": "#AAAAAA",
      "8": "#555555",
      "9": "#5555FF",
      "a": "#55FF55",
      "b": "#55FFFF",
      "c": "#FF5555",
      "d": "#FF55FF",
      "e": "#FFFF55",
      "f": "#FFFFFF",
    };
    let color = null;
    let bold = false;
    let italic = false;
    let underline = false;
    let strike = false;

    function style() {
      const parts = [];
      if (color) parts.push(`color:${color}`);
      if (bold) parts.push("font-weight:700");
      if (italic) parts.push("font-style:italic");
      if (underline || strike) {
        const dec = [];
        if (underline) dec.push("underline");
        if (strike) dec.push("line-through");
        parts.push(`text-decoration:${dec.join(" ")}`);
      }
      return parts.join(";");
    }

    let out = "";
    let buf = "";
    function flush() {
      if (!buf) return;
      const st = style();
      const content = escapeHtml(buf).replace(/\n/g, "<br/>");
      out += st ? `<span style="${st}">${content}</span>` : content;
      buf = "";
    }

    for (let i = 0; i < s.length; i++) {
      const ch = s[i];
      if (ch === "§" && i + 1 < s.length) {
        flush();
        const code = s[i + 1].toLowerCase();
        i++;
        if (colors[code]) {
          color = colors[code];
        } else if (code === "l") {
          bold = true;
        } else if (code === "o") {
          italic = true;
        } else if (code === "n") {
          underline = true;
        } else if (code === "m") {
          strike = true;
        } else if (code === "r") {
          color = null;
          bold = false;
          italic = false;
          underline = false;
          strike = false;
        }
        continue;
      }
      buf += ch;
    }
    flush();
    return out;
  }

  const lines = [];
  if (spec.sign1) lines.push(`**sign1:** ${spec.sign1}`);
  if (spec.sign2) lines.push(`**sign2:** ${spec.sign2}`);
  if (spec.gui) lines.push(`**gui:** ${spec.gui}`);
  if (spec.aliases && spec.aliases.length) lines.push(`**aliases:** ${spec.aliases.join(", ")}`);
  if (spec.description) {
    lines.push("");
    lines.push("**description:**");
    lines.push("```");
    lines.push(spec.description);
    lines.push("```");
  }
  if (spec.descriptionRaw) {
    const html = mcToHtml(spec.descriptionRaw);
    if (html) {
      lines.push("");
      lines.push("**description (mc colors):**");
      lines.push(`<div style="font-family: var(--vscode-editor-font-family); font-size: 12px; line-height: 1.35;">${html}</div>`);
    }
  }
  if (spec.params && spec.params.length) {
    lines.push("");
    lines.push("**params:**");
    for (const p of spec.params) {
      lines.push(`- \`${p.name}\` (${p.mode}) slot ${p.slot}`);
    }
  }
  if (spec.enums && spec.enums.length) {
    lines.push("");
    lines.push("**enums:**");
    for (const e of spec.enums) {
      lines.push(`- \`${e.name}\` slot ${e.slot}`);
    }
  }
  const md = new vscode.MarkdownString(lines.join("\n"));
  md.supportHtml = true;
  md.isTrusted = true;
  return md;
}

function activate(context) {
  let api = {};
  let lookup = {};
  let statusItem = null;

  function reloadApi(reason) {
    const { apiAliasesPath, docsRoot } = getConfig();
    api = loadApi();
    lookup = buildLookup(api);
    output.appendLine(`[reload] ${reason || "manual"}`);
    output.appendLine(`  apiAliasesPath=${apiAliasesPath}`);
    output.appendLine(`  docsRoot=${docsRoot}`);
    output.appendLine(`  apiLoadedModules=${Object.keys(api).length}`);
    if (apiAliasesPath && !fs.existsSync(apiAliasesPath)) {
      output.appendLine(`  WARN: apiAliasesPath does not exist`);
    }
    if (docsRoot && !fs.existsSync(docsRoot)) {
      output.appendLine(`  WARN: docsRoot does not exist`);
    }
  }

  reloadApi("activate");
  output.show(true);

  context.subscriptions.push(vscode.commands.registerCommand("mldsl.reloadApi", () => reloadApi("command")));

  function findCompilerPath() {
    const { compilerPath } = getConfig();
    if (compilerPath && fs.existsSync(compilerPath)) return compilerPath;

    const folders = vscode.workspace.workspaceFolders || [];
    if (!folders.length) return null;
    const root = folders[0].uri.fsPath;
    const auto = path.join(root, "tools", "mldsl_compile.py");
    if (fs.existsSync(auto)) return auto;
    return null;
  }

  function resolvePlanPath() {
    const { planPath } = getConfig();
    if (planPath && String(planPath).trim()) return String(planPath).trim();
    const appdata = process.env.APPDATA || process.env.appdata;
    if (appdata) return path.join(appdata, ".minecraft", "plan.json");
    return path.join(process.cwd(), "plan.json");
  }

  async function compileAndCopy() {
    const id = ++seq;
    const ed = vscode.window.activeTextEditor;
    if (!ed || !ed.document) {
      vscode.window.showWarningMessage("MLDSL: No active editor");
      return;
    }
    if (ed.document.languageId !== "mldsl") {
      vscode.window.showWarningMessage("MLDSL: Not an .mldsl file");
      return;
    }

    await ed.document.save();

    const compiler = findCompilerPath();
    const { pythonPath } = getConfig();
    if (!compiler) {
      vscode.window.showErrorMessage(
        "MLDSL: compiler not found. Set mldsl.compilerPath or open the mlctmodified workspace root."
      );
      output.appendLine(`[compile#${id}] compiler missing (config.compilerPath not found; auto-detect failed)`);
      return;
    }

    const filePath = ed.document.uri.fsPath;
    output.appendLine(`[compile#${id}] ${pythonPath} ${compiler} ${filePath}`);

    const env = Object.assign({}, process.env, { PYTHONIOENCODING: "utf-8" });

    cp.execFile(pythonPath || "python", [compiler, filePath], { env }, async (err, stdout, stderr) => {
      if (stderr && String(stderr).trim()) {
        output.appendLine(`[compile#${id}] stderr: ${String(stderr).trim()}`);
      }
      if (err) {
        output.appendLine(`[compile#${id}] ERROR: ${err.message || String(err)}`);
        vscode.window.showErrorMessage("MLDSL: Compile failed (see Output → MLDSL Helper)");
        return;
      }
      const text = String(stdout || "").trim();
      if (!text) {
        vscode.window.showWarningMessage("MLDSL: Compiler produced empty output");
        return;
      }
      await vscode.env.clipboard.writeText(text);
      const lines = text.split(/\r?\n/).filter((x) => x.trim()).length;
      vscode.window.showInformationMessage(`MLDSL: Copied ${lines} command(s) to clipboard`);
      output.appendLine(`[compile#${id}] ok lines=${lines}`);
    });
  }

  async function compilePlan() {
    const id = ++seq;
    const ed = vscode.window.activeTextEditor;
    if (!ed || !ed.document) {
      vscode.window.showWarningMessage("MLDSL: No active editor");
      return;
    }
    if (ed.document.languageId !== "mldsl") {
      vscode.window.showWarningMessage("MLDSL: Not an .mldsl file");
      return;
    }

    await ed.document.save();

    const compiler = findCompilerPath();
    const { pythonPath } = getConfig();
    if (!compiler) {
      vscode.window.showErrorMessage(
        "MLDSL: compiler not found. Set mldsl.compilerPath or open the mlctmodified workspace root."
      );
      output.appendLine(`[plan#${id}] compiler missing (config.compilerPath not found; auto-detect failed)`);
      return;
    }

    const filePath = ed.document.uri.fsPath;
    const outPlan = resolvePlanPath();
    output.appendLine(`[plan#${id}] ${pythonPath} ${compiler} --plan ${outPlan} ${filePath}`);

    const env = Object.assign({}, process.env, { PYTHONIOENCODING: "utf-8" });

    cp.execFile(pythonPath || "python", [compiler, "--plan", outPlan, filePath], { env }, async (err, stdout, stderr) => {
      if (stderr && String(stderr).trim()) {
        output.appendLine(`[plan#${id}] stderr: ${String(stderr).trim()}`);
      }
      if (err) {
        output.appendLine(`[plan#${id}] ERROR: ${err.message || String(err)}`);
        vscode.window.showErrorMessage("MLDSL: Compile plan failed (see Output → MLDSL Helper)");
        return;
      }
      await vscode.env.clipboard.writeText(`/mldsl run \"${outPlan}\"`);
      vscode.window.showInformationMessage(`MLDSL: Wrote plan.json and copied /mldsl run to clipboard`);
      output.appendLine(`[plan#${id}] ok wrote=${outPlan}`);
    });
  }

  context.subscriptions.push(vscode.commands.registerCommand("mldsl.compileAndCopy", compileAndCopy));
  context.subscriptions.push(vscode.commands.registerCommand("mldsl.compilePlan", compilePlan));
  context.subscriptions.push(
    vscode.workspace.onDidChangeConfiguration((e) => {
      if (
        e.affectsConfiguration("mldsl.apiAliasesPath") ||
        e.affectsConfiguration("mldsl.docsRoot") ||
        e.affectsConfiguration("mldsl.pythonPath") ||
        e.affectsConfiguration("mldsl.compilerPath") ||
        e.affectsConfiguration("mldsl.planPath")
      ) {
        reloadApi("config");
      }
    })
  );

  const completionProvider = vscode.languages.registerCompletionItemProvider(
    { language: "mldsl" },
    {
      provideCompletionItems(document, position) {
        const id = ++seq;
        const line = document.lineAt(position.line).text;
        const info = findModuleAndPrefix(line, position.character);
        if (!info) {
          output.appendLine(`[completion#${id}] no module prefix match`);
          return;
        }

        const mod = lookup[info.module];
        if (!mod) {
          output.appendLine(`[completion#${id}] module not found: ${info.module}`);
          return;
        }

        const items = [];
        for (const [alias, entry] of Object.entries(mod.byName)) {
          if (info.prefix && !alias.startsWith(info.prefix)) continue;
          const funcName = entry.funcName;
          const spec = entry.spec;
          const item = new vscode.CompletionItem(alias, vscode.CompletionItemKind.Function);
          const params = (spec.params || []).map((p) => p.name).join(", ");
          item.detail = `${info.module}.${funcName}(${params})`;
          if (alias !== funcName) {
            item.detail += `  (alias of ${funcName})`;
          }
          item.documentation = specToMarkdown(spec);
          items.push(item);
        }
        output.appendLine(
          `[completion#${id}] ${info.module}. prefix='${info.prefix}' items=${items.length}`
        );
        return items;
      },
    },
    "."
  );

  const hoverProvider = vscode.languages.registerHoverProvider({ language: "mldsl" }, {
    provideHover(document, position) {
      const id = ++seq;
      const q = findQualifiedAtPosition(document, position);
      if (!q) return;
      const mod = lookup[q.module];
      if (!mod) return;
      const entry = mod.byName[q.func];
      if (!entry) return;
      output.appendLine(`[hover#${id}] ${q.text} -> ${q.module}.${entry.funcName}`);
      return new vscode.Hover(specToMarkdown(entry.spec), q.range);
    }
  });

  const defProvider = vscode.languages.registerDefinitionProvider({ language: "mldsl" }, {
    provideDefinition(document, position) {
      const id = ++seq;
      const q = findQualifiedAtPosition(document, position);
      if (!q) return;
      const mod = lookup[q.module];
      if (!mod) {
        output.appendLine(`[def#${id}] module not found for ${q.text}`);
        return;
      }
      const entry = mod.byName[q.func];
      if (!entry) {
        output.appendLine(`[def#${id}] function not found for ${q.text}`);
        // show a few keys for debugging
        const keys = Object.keys(mod.byName).slice(0, 30);
        output.appendLine(`[def#${id}] known keys sample: ${keys.join(", ")}`);
        return;
      }
      const { docsRoot } = getConfig();
      const docPath = path.join(docsRoot || "", q.module, `${entry.funcName}.md`);
      if (!docsRoot) {
        output.appendLine(`[def#${id}] docsRoot not set`);
        return;
      }
      if (!fs.existsSync(docPath)) {
        output.appendLine(`[def#${id}] doc not found: ${docPath}`);
        return;
      }
      output.appendLine(`[def#${id}] ${q.text} -> ${docPath}`);
      const uri = vscode.Uri.file(docPath);
      return new vscode.Location(uri, new vscode.Position(0, 0));
    }
  });

  const diagnostics = vscode.languages.createDiagnosticCollection("mldsl");

  function updateDiagnostics(doc) {
    if (!doc || doc.languageId !== "mldsl") return;
    const diags = [];
    const re = /([a-zA-Z_][\w]*)\.([\w\u0400-\u04FF]+)/g;
    for (let lineNum = 0; lineNum < doc.lineCount; lineNum++) {
      const line = doc.lineAt(lineNum).text;
      let m;
      while ((m = re.exec(line))) {
        const moduleName = m[1];
        const funcName = m[2];
        const range = new vscode.Range(
          new vscode.Position(lineNum, m.index),
          new vscode.Position(lineNum, m.index + m[0].length)
        );
        const mod = lookup[moduleName];
        if (!mod) {
          diags.push(new vscode.Diagnostic(range, `Unknown module '${moduleName}'`, vscode.DiagnosticSeverity.Warning));
          continue;
        }
        const entry = mod.byName[funcName];
        if (!entry) {
          // Don't warn on partial typing: player.соо (prefix of player.сообщение)
          const keys = Object.keys(mod.byName);
          const hasPrefix = keys.some((k) => k.startsWith(funcName));
          if (hasPrefix) {
            continue;
          }
          diags.push(
            new vscode.Diagnostic(
              range,
              `Unknown function '${moduleName}.${funcName}'`,
              vscode.DiagnosticSeverity.Warning
            )
          );
        }
      }
    }
    diagnostics.set(doc.uri, diags);
  }

  context.subscriptions.push(diagnostics);
  context.subscriptions.push(vscode.workspace.onDidOpenTextDocument((doc) => updateDiagnostics(doc)));
  context.subscriptions.push(
    vscode.workspace.onDidChangeTextDocument((e) => updateDiagnostics(e.document))
  );
  context.subscriptions.push(vscode.window.onDidChangeActiveTextEditor((ed) => ed && updateDiagnostics(ed.document)));

  function updateStatusBar() {
    const ed = vscode.window.activeTextEditor;
    const ok = ed && ed.document && ed.document.languageId === "mldsl";
    if (!statusItem) {
      statusItem = vscode.window.createStatusBarItem(vscode.StatusBarAlignment.Left, 100);
      statusItem.command = "mldsl.compileAndCopy";
      context.subscriptions.push(statusItem);
    }
    if (ok) {
      statusItem.text = "MLDSL: Compile";
      statusItem.tooltip = "Compile current .mldsl and copy /placeadvanced command(s) to clipboard (or use MLDSL: Compile to plan.json)";
      statusItem.show();
    } else {
      statusItem.hide();
    }
  }

  context.subscriptions.push(vscode.window.onDidChangeActiveTextEditor(() => updateStatusBar()));
  updateStatusBar();

  context.subscriptions.push(completionProvider, hoverProvider, defProvider);
}

function deactivate() {}

module.exports = { activate, deactivate };
