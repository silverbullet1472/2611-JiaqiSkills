# Jiaqi Skills

个人维护的 Codex Skills，按使用场景独立安装。

| Skill | 用途 |
|---|---|
| [ai-native-project](ai-native-project/SKILL.md) | 初始化或维护AI项目目录、工作约定与状态记录 |
| [finalize-project](finalize-project/SKILL.md) | 整理验证成果、归档，并处理范围内的Git提交 |
| [handoff-session](handoff-session/SKILL.md) | 保存工作进度，准备新会话交接 |
| [human-presentation](human-presentation/SKILL.md) | 优化汇报页面的文案、信息层级与图文关系 |
| [wangxin-presentation](wangxin-presentation/SKILL.md) | 制作网信中心风格的HTML汇报，包含模板、素材与播放器 |
| [work-reports](work-reports/SKILL.md) | 根据项目记录写周报，或根据周报文字汇总月报 |

## 安装与调用

将需要的整个Skill文件夹复制到个人技能目录：

- Windows：`%USERPROFILE%\.codex\skills\`
- macOS / Linux：`~/.codex/skills/`
- 设置了`CODEX_HOME`时，使用`$CODEX_HOME/skills/`。

目录结构应为`skills/<技能名>/SKILL.md`。保留该技能文件夹里的`assets`、`references`、`scripts`和`agents`等配套文件，不要只复制`SKILL.md`。避免覆盖已经修改过的同名技能。

安装后在后续消息中使用`$技能名`，例如：

```text
使用 $work-reports，根据当前项目工作记录写上周周报。
```

```text
使用 $wangxin-presentation，根据提供的材料制作网信中心风格HTML汇报。
```

## 网信中心汇报说明

默认采用电脑端16∶9分页HTML，图片和播放器内嵌，支持目录跳转、翻页、图片放大、全屏及打印PDF。MiSans通过小米官方服务在线加载，失败时回退微软雅黑等系统字体；断网仍可演示，字形可能不同。文案与版式规则已经包含在该Skill内，无需调用`human-presentation`。

字体使用说明、原始视觉素材出处及制作接口见该技能的`references/`。本仓库未包含原业务汇报的输入数据或试用HTML。

## 个人全局工作约定

[AGENTS.md](AGENTS.md)是个人全局工作偏好的原样备份，涵盖中文表达、任务范围、代码复杂度、验证投入和子代理协作方式。

如需用作个人全局配置，可放到`~/.codex/AGENTS.md`（Windows对应`%USERPROFILE%\.codex\AGENTS.md`，设置了`CODEX_HOME`时使用该目录）。已有配置时先比较、按需合并，避免直接覆盖自己的习惯。文中的模型、子代理类型与工作流程取决于使用环境，不保证适用于每个人。
