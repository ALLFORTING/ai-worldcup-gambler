# ⚽ 赌狗的自我修养 · AI World Cup Gambler

## 简介

`ai-worldcup-gambler` 是一个给 AI agent 玩的虚拟世界杯赌球模拟器。它采用单文件核心逻辑和纯文本命令交互：外部调用只需要 `gambler.cmd(command_string)`。

你从 100000 虚拟资金开始，面对 16 支虚构球队、完整小组赛和淘汰赛、庄家抽水赔率、新闻传闻、高利贷、称号和下注历史。长期期望值是负的，因为庄家不是来做公益的。

本项目参考 [Asti-Z/leek](https://github.com/Asti-Z/leek) 的单文件交互设计模式，但实现内容为独立项目。

## 免责声明

这是一个虚拟游戏，不涉及真实金钱，不提供任何现实赌博建议，也不鼓励真实赌博。项目中的讽刺、调侃和“赌狗”文本只用于虚拟模拟器氛围。

现实里请远离赌博。现实里的庄家不会因为你 README 写得好就放过你。

## 功能特性

- 16 支虚构世界杯球队，分为 4 个实力档位。
- 小组赛 + 淘汰赛完整赛制，共 34 场比赛、17 轮下注机会。
- 支持胜平负、猜比分、总进球、点球大战、串关下注。
- 基于真实概率生成赔率，并加入庄家抽水和每轮 ±5% 波动。
- 自定义 mulberry32 PRNG，支持确定性随机：同 seed + 同操作 = 同结果。
- 新闻/传闻系统：影响玩家认知，但不直接改变比赛结果。
- 高利贷系统：现金归零后可借 50000，每轮 10% 复利。
- 称号系统：动态资产称号和永久行为称号。
- 下注历史、盈亏追踪、胜率统计。
- JSON 存档/读档，自动生成 `gambler_save.json`。
- 纯标准库实现，不需要安装第三方依赖。

## 项目结构

```text
ai-worldcup-gambler/
├── gambler.py
├── README.md
├── LICENSE
├── .gitignore
├── examples/
│   ├── demo.py
│   └── full_demo.py
├── tests/
│   ├── smoke_test.py
│   └── full_run_test.py
└── .github/
    └── workflows/
        └── smoke-test.yml
```

`gambler.py` 是核心文件，所有游戏逻辑都集中在这个文件里。`gambler_save.json` 是运行时自动生成的存档文件，不应提交到 GitHub。

## 安装方式

克隆仓库后直接运行即可：

```bash
git clone https://github.com/ALLFORTING/ai-worldcup-gambler.git
cd ai-worldcup-gambler
python examples/demo.py
python examples/full_demo.py
```

运行项目不需要安装第三方依赖，只使用 Python 标准库。

## 快速开始

```python
import gambler

print(gambler.cmd("new_game 12345"))
print(gambler.cmd("help"))
print(gambler.cmd("schedule"))
print(gambler.cmd("news"))
print(gambler.cmd("bet wnl 1 home 5000"))
print(gambler.cmd("next"))
print(gambler.cmd("status"))
```

## 完整演示

运行：

```bash
python examples/full_demo.py
```

它会用固定 seed 自动跑完整 17 轮，展示完整世界杯流程、自动下注、结算、最终状态、称号和历史。这个脚本不追求聪明，只负责把游戏从开幕吹到决赛，顺便让庄家露出职业微笑。

## 测试

本项目不依赖第三方测试框架，可以直接运行：

```bash
python tests/smoke_test.py
python tests/full_run_test.py
```

GitHub Actions 会在 push 和 pull request 时自动运行 smoke test、full run test 和 demo。

## 命令列表

```text
help
status
schedule
standings
news
bet wnl 1 home 5000
bet score 1 2-1 1000
bet goals 1 over3 2000
bet pk 1 yes 1000
parlay 1,2,3 home,away,home 3000
next
history
titles
loan
repay 10000
quit
new_game 12345
```

## 游戏规则

玩家初始资金为 100000。单次下注最低 100，资金不足时不能下注。每轮比赛开始前可以查看赛程、赔率和新闻，然后下注。执行 `next` 后会模拟当前轮所有比赛，结算本轮下注，更新资金、债务、积分榜、淘汰赛晋级、称号和下注历史。

如果现金小于等于 0，可以执行 `loan` 借高利贷。每次固定借款 50000，每轮 10% 复利。净资产或债务触及危险红线后游戏会强制结束。也可以执行 `quit` 直接结束游戏。

## 赛制说明

16 支球队分为 4 档：

```text
brazilia / Brazilia 92
argentino / Argentino 90
franch / Franch 89
germeny / Germeny 87
espanya / Espanya 85
englund / Englund 84
portugalo / Portugalo 83
belgica / Belgica 82
nederlund / Nederlund 80
kroatia / Kroatia 79
uruguayo / Uruguayo 78
italio / Italio 77
japon / Japón 74
koreo / Koreo 73
mexica / Mexica 72
merican / Merican 71
```

分组为 A/B/C/D 四组，每组 4 队，每组包含不同档位球队。分组受 seed 控制，可复现。

小组赛每组单循环，共 24 场。每轮 2 场比赛，共 12 轮。胜 3 分、平 1 分、负 0 分。排名规则为积分、净胜球、进球数、球队 power 和稳定 tie-breaker。

淘汰赛共 5 轮 10 场：8 强赛、4 强赛、半决赛、三四名决赛、决赛。90 分钟可以打平，但淘汰赛必须通过加时或点球产生胜者。

## 下注玩法

### 胜平负

```text
bet wnl <match_index> <home/draw/away> <amount>
```

小组赛和淘汰赛都支持。淘汰赛的胜平负指 90 分钟赛果，不等同于最终晋级。

### 猜比分

```text
bet score <match_index> <score> <amount>
```

示例：`bet score 1 2-1 1000`。比分玩法赔率较高，抽水也更狠。

### 总进球

```text
bet goals <match_index> <overN/underN> <amount>
```

示例：`over3` 表示总进球数严格大于 3，`under3` 表示严格小于 3。

### 点球大战

```text
bet pk <match_index> <yes/no> <amount>
```

仅淘汰赛可用。小组赛使用会返回错误提示。

### 串关

```text
parlay 1,2,3 home,away,home 3000
```

所有场次都猜中才赢。赔率为各项赔率相乘，并加入累积抽水。

## 存档机制

游戏会自动在项目目录生成 `gambler_save.json`。每次新开局、下注、推进轮次、借款、还款或退出都会写入存档。存档包含 PRNG 状态，因此读档后继续操作仍保持确定性。

`.gitignore` 已忽略 `gambler_save.json`，不要把它提交到 GitHub。

## 示例输出

```text
>>> schedule
🗓️ 当前赛程：第 1 / 17 轮 · 小组赛 A组第1轮
下注编号只在当前轮有效。赔率已经抽水，别幻想长期正期望。

[1] Brazilia vs Mexica | 小组赛 A组第1轮
  胜平负：home 1.42 / draw 3.58 / away 5.90
  总进球：over2 1.66 / under3 2.11 / over3 2.42 / under4 1.67
  比分示例：1-0 6.52 / 2-1 8.44 / 1-1 7.30 / 0-1 14.20
```

具体输出会随 seed 和操作序列变化。

## 给 AI Agent 的使用方式

AI agent 不需要解析图形界面，也不需要安装依赖。直接通过纯文本命令循环调用：

```python
import gambler

response = gambler.cmd("new_game 12345")
print(response)

response = gambler.cmd("schedule")
print(response)

response = gambler.cmd("bet wnl 1 home 5000")
print(response)
```

所有返回值都是字符串，适合 agent 读取、总结、决策和继续调用。`gambler_save.json` 会自动生成，agent 不需要手动创建。

## 开发说明

- 核心逻辑全部位于 `gambler.py`。
- 外部交互入口只有 `cmd(command_string: str) -> str`。
- 不依赖第三方包。
- 随机数不使用 Python 全局 `random`，而是使用自定义 mulberry32。
- 所有随机过程都通过游戏状态内的 PRNG，存档保存 PRNG 状态。
- 输出为纯文本，适合命令行、人类和 AI agent。

## License

MIT License. See [LICENSE](LICENSE).
