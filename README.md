# 拉康视角 · lacan-lens · v1.1.0

用于中文文本解释和经同意的自我探索：提供可质疑的假设、可定位的来源与现实替代解释。不是拉康角色扮演、心理诊断或精神分析治疗。

**公开发布版。** 由 Rockiez 维护，使用 Hermes Agent 辅助整理。25组审查均有处置结论，不等于全部原典已证实；支持5组、需限定19组、未核实1组。

## 使用示例（均为通用虚构输入）
- “请用拉康视角读一则寓言：角色总希望得到评委肯定。区分文本事实与解释，并给一种非拉康解释。”
- “对象a为什么不直接等于角色想拿到的奖杯？请标出概念时期和可定位来源。”
- “比较XI的穿越幻想与XXIII的sinthome，不要把它们排成自助成长阶段。”
- “请列四话语的四个位置，并说明表头命名的历史限制。”
- “停止这个视角，只整理故事情节。”——应立即停止理论解释。

## 手动通用安装
1. 先阅读 [SKILL.md](SKILL.md)、[NOTICE](NOTICE.md) 和 [许可说明](LICENSE.md)，确认接受解释性工具的边界。
2. 根据你的运行器文档确认**当前配置或profile实际使用的技能目录**，不要猜固定本机路径。Hermes以 [官方文档](https://hermes-agent.nousresearch.com/docs/) 为准；其他兼容运行器按各自文档操作。
3. 在该技能目录中建立 `lacan-lens` 文件夹，把本包的 `SKILL.md`、`references/`、`scripts/` 及许可/说明文件一起复制进去，保留相对结构。替换旧版前先备份，避免影响别的profile。
4. 按运行器文档刷新技能索引或重新加载；确认它确实能读取版本1.1.0及关联参考文件。这里不猜测安装或刷新命令，不把复制文件等同加载成功。
5. 纯提示运行器可直接加载SKILL.md并提供关联参考文件；不能检索来源时必须标注未核实。日常使用无需额外Python依赖；验证脚本需要Python 3.9或更高版本，仅标准库。

## 本地验证
在包根目录运行 `python3 scripts/validate.py`，Windows等环境可使用实际可用的Python启动器。Hermes中可调用 `terminal(command="python3 scripts/validate.py")`。

验证相对引用、25组覆盖和分类计数、四话语位置、关键限定、隐私线索、意外文件及GitHub URL结构。它不联网，不验证远端HTTP可达性，不证明没有任何未知隐私信息，也不替代学术或行为审查。人工行为案例见 [acceptance-cases](references/acceptance-cases.md)。

## 文件与审查
- [SKILL.md](SKILL.md)：可加载的技能正文。
- [source-audit](references/source-audit.md)：署名、来源层级、固定版本及缺口。
- [comprehensive-audit](references/comprehensive-audit.md)：25组结论及证据定位，无长引文或源副本。
- [CHANGELOG](CHANGELOG.md)：修订记录；[NOTICE](NOTICE.md) 与 [LICENSE](LICENSE.md)：权利边界。

## 发布与许可
- 仓库：https://github.com/Rockiez/lacan-lens
- 新增与改写内容沿用 CC BY 4.0；第三方权利与署名见 NOTICE.md 和 LICENSE.md。
- 静态检查不等于模型行为、完整原典或临床有效性验证。
