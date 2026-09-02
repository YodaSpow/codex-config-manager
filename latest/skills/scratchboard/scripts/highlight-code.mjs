import { codeToHtml } from "shiki";

const [language = "text"] = process.argv.slice(2);
let source = "";
process.stdin.setEncoding("utf8");
process.stdin.on("data", (part) => { source += part; });
process.stdin.on("end", async () => {
  try {
    process.stdout.write(await codeToHtml(source, { lang: language, theme: "github-dark" }));
  } catch {
    process.exitCode = 1;
  }
});
