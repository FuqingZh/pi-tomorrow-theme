# Tomorrow Theme for Pi

[English](README.md) · 简体中文

将 [Chris Kempson 的五款 Tomorrow 主题][upstream] 移植到 Pi。

**最低支持 Pi 0.99.0。** 更早的版本可能可以加载基础配色，但不能识别主题声明的亮色或暗色外观。详见[兼容性记录](docs/reference/pi-compatibility.md)。

| 主题 | Pi 中的名称 | 搭配的终端底色 |
| --- | --- | --- |
| Tomorrow | `tomorrow` | `#ffffff` |
| Tomorrow Night | `tomorrow-night` | `#1d1f21` |
| Tomorrow Night Eighties | `tomorrow-night-eighties` | `#2d2d2d` |
| Tomorrow Night Blue | `tomorrow-night-blue` | `#002451` |
| Tomorrow Night Bright | `tomorrow-night-bright` | `#000000` |

## 安装

通过 Pi 从 npm 安装：

```sh
pi install npm:pi-tomorrow-theme
```

也可以直接从 GitHub 安装：

```sh
pi install git:github.com/FuqingZh/pi-tomorrow-theme
```

任选一个来源。重启 Pi 或运行 `/reload`，再到 **`/settings` → Theme** 选择主题。

## 从本地仓库试用

在仓库根目录运行：

```sh
pi --theme ./themes --use-theme tomorrow-night-eighties
```

可以将最后一个参数换成表里的任意名称。这个命令不会改动已保存的主题设置。

要还原原版观感，请在支持真彩色的终端里配上表中的底色，尤其是浅色版
`tomorrow`。Pi 主题只为 Pi 绘制的区域配色，不改变普通助手回复后方或留白处的默认终端底色。

## 无需调用模型的预览

在仓库根目录运行以下命令，用临时 Pi 配置回放示例会话。看完直接退出，不用提交提示词。
可将 `--use-theme` 换成表里的主题名，也可以用 `dark` 对照 Pi 的内置主题。

```sh
(
  repo=$PWD
  scratch=$(mktemp -d) || exit 1
  trap 'rm -rf -- "$scratch"' EXIT
  cp "$repo/test/fixtures/preview.jsonl" "$scratch/preview.jsonl" || exit 1
  cd "$scratch" || exit 1
  PI_CODING_AGENT_DIR="$scratch/agent" PI_OFFLINE=1 pi --no-extensions --no-skills \
    --theme "$repo/themes" --use-theme tomorrow-night-blue \
    --session "$scratch/preview.jsonl"
)
```

## 配色和署名

每款主题都保留 [Xresources][palette] 的 12 个原始色值，代码配色参考
[TextMate 移植版][textmate]。代码注释使用原色；Pi 特有的面板、标题和工具输出在需要时
使用同色系的其他色阶。Night Blue 的深蓝面板参考了 VS Code 版。所有变体都保留 Pi 原生的粗体显示。

[项目文档](docs/README.md)说明了设计和验证方法。原主题版权归 © 2011 Chris Kempson，
采用 [MIT 许可](LICENSE)。

[upstream]: https://github.com/chriskempson/tomorrow-theme
[palette]: https://github.com/chriskempson/tomorrow-theme/tree/ccf6666/Xdefaults
[textmate]: https://github.com/chriskempson/tomorrow-theme/tree/ccf6666/textmate
