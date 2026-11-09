# 视觉与制作约定

## 参考画面

制作前查看与本次页面有关的图片：[封面](reference-cover.jpg)、[目录](reference-contents.jpg)、[正文](reference-body.jpg)、[结束页](reference-closing.jpg)。这些是用户提供的PPT实际渲染图，只用于风格判断，不把整页截图当作新汇报。

## 页面外框

1600×900设计画布，等比缩放到桌面窗口，不对手机重排。主导航高72px、字号40px，深蓝到青蓝渐变；二级导航高52px、字号27px，浅灰底。字号按原PPT的24pt/16pt及页面宽度换算，保留原导航在画面中的分量。主导航当前项白字，其他项浅蓝字；二级当前项深蓝，其他项青蓝。两级导航均不加下划线，以文字颜色区分当前项。两级导航只显示章节和主题名称，不加数字编号。正式目录保留原有编号块。导航可点击跳转。导航文字长度应适合内容分组，避免缩成难读的小字。

正文左右62px安全边距，标题顶部152px，标题42px/粗体，左侧橙黄色竖条。正文起点228px，高626px；普通文字24～28px，图注16～19px，按内容而非固定字数排版。页码位于右下，单位位于左下。默认中英文、数字使用在线MiSans VF，可变字重对应现有正文和标题；失败时依次回退微软雅黑、苹方、系统无衬线字体。既有正文中单独指定的微软雅黑、Arial和Georgia由生成器统一为该字体栈。深蓝、青蓝用于层级；橙黄色只作标题识别或少量重点，不把页面涂成多色看板。

背景使用`map-background.jpg`，居中显示，宽度为画布的80%，不透明度33.5%；正文与结束页一致，文字区保持干净。原图已经很浅，不需要额外锐化或强化地图。图表、截图和表格上方不叠水印。

## 特殊页面

- 封面：使用`cover-ribbon.png`保留曲面造型；左侧三张圆形照片分别为建筑、坝体、河流；中右部白色标题86px、行高1.35、顶距330px，底部单位日期28px。标题保持完整语义分行，在蓝色区域形成视觉重心；长标题优先调整换行，不为了塞进一行而过度缩小字号，不能挤进装饰区。
- 目录：浅灰左区列编号和章节，目录标题86px、条目40px、编号42px；右侧`building-landscape.jpg`，青色斜带和少量斜块呼应PPT。编号用于章节索引。目录条目可点击。
- 结束：白底淡地图，“请批评指正，谢谢！”或用户指定文字，字号80px，单位日期28px，`closing-river.png`填充到`closing-frame.svg`的原PPT自由曲线路径中，保留上下不规则轮廓及浅蓝曲线衬边，不能直接铺成矩形横幅，底部单位日期。不新增宣传口号。

## 素材出处

均由用户授权从“数字孪生处-面向河湖遥感图斑复核的AI辅助研判技术研究-v2.pptx”抽取：

| 本目录素材 | PPT包内文件 | 用途 |
|---|---|---|
| map-background.jpg | ppt/media/image1.jpeg | 正文与结束底纹 |
| cover-ribbon.png | ppt/media/image2.png | 封面曲面 |
| building-portrait.jpg | ppt/media/image3.jpeg | 封面建筑圆图 |
| dam.jpg | ppt/media/image4.jpeg | 封面坝体圆图 |
| river.jpg | ppt/media/image5.jpeg | 封面河流圆图 |
| building-landscape.jpg | ppt/media/image6.jpeg | 目录建筑照片 |
| closing-river.png | ppt/media/image8.png | 结束页水景 |

保持原始文件，HTML中用裁切和尺寸控制构图。不要把业务截图、人员名单或旧数据存为通用模板素材。

`closing-frame.svg`的两条路径直接取自原PPT结束页版式`ppt/slideLayouts/slideLayout6.xml`中的自定义几何形状，并按原组合坐标换算；生成器内嵌照片，保留曲线裁切及渐变衬边。

## 在线字体

使用小米官网实际使用的CSS接口：`https://cdn-font.hyperos.mi.com/font/css?family=MiSans_VF:VF:Chinese_Simplify,Latin&display=swap`，返回的字体族名为`MiSans VF`。不要误写成未定义的`MiSans`。通过HTML的stylesheet链接在页面样式之前加载，不把`@import`追加在既有CSS末尾；两个官方字体域名配置preconnect。

该接口按Unicode范围分包，浏览器按所需字符加载。`font-display: swap`允许字体未到达时先显示备用字体，成功后切换；网络失败不阻止演示。此模式不保证完全相同的离线字形，不能再宣称字体也完全离线。检查排版时等待`document.fonts.ready`，确认实际渲染为MiSans；另用无缓存浏览器上下文屏蔽字体网络，验证微软雅黑回退和页面边界。打印前等待字体加载完成。

官方来源：`https://hyperos.mi.com/font/zh/`及其样式表。许可协议见`https://hyperos.mi.com/font-download/MiSans字体知识产权许可协议.pdf`；保留页面head中的MiSans使用声明。在线方案不重新分发或改造字体文件，不在页面画面增加字体来源入口。
