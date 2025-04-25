# ZhaDanRen 游戏项目（炸弹人）

## 项目简介
ZhaDanRen 是一款基于 Pygame 开发的多人竞技类策略游戏，灵感来源于经典街机游戏《炸弹人》（Bomberman）。玩家通过放置炸弹、控制爆炸范围和收集道具，在充满障碍的迷宫中击败对手或达成目标。游戏支持多地图、角色选择和复杂的 AI 对战系统，具有以下核心功能：
- **多角色选择**：玩家可选择不同颜色的角色（蓝/绿/草/紫）进行游戏。
- **动态地图系统**：内置多张可破坏墙体的地图（gmap1-6），支持障碍物交互。
- **道具系统**：包含血量恢复、爆炸范围扩展、遥控炸弹等10+种道具效果。
- **AI 敌人系统**：基于 A* 算法的智能敌人，会主动追击玩家并规划路径。
- **状态管理**：通过状态机实现游戏流程控制（主界面/设置/游戏/结束）。

---
## 游戏教程
### 选人界面
鼠标放在人物上单击左键变为锁定状态，双击则变为解锁状态， 锁定锁定状态才能进入选择地图界面
### 选择地图界面
可以从左侧列表中选择地图，右侧是地图缩略图，地图里面的箭头则是玩家出生地
###  游戏操作
- *移动操作*： **w:向上移动; s:向下移动;a:像左移动;d:向右移动**
- *放置炸弹操作*： **按j放置炸弹，如有遥控炸弹时，短按j放置，长按j引爆**
### 道具说明
- *心*：**加一个最大生命值**
- *炸弹*： **加一个最大炸弹数量**
- *拳套*： **加一格爆炸范围**
- *护盾*：**无敌5秒时间**
- *遥控器*： **将你的炸弹变为遥控炸弹，数量为你的最大炸弹数量，用完就会变成普通炸弹**

---

## 环境要求
- Python 3.8+
- Pygame-ce 2.5+
- Pygame_gui 0.9.54+

# ZhaDanRen Game Project (Bomberman)

## Project Introduction
ZhaDanRen is a multiplayer strategy game developed using Pygame, inspired by the classic arcade game Bomberman. Players place bombs, control explosion ranges, and collect items to defeat opponents or achieve goals in maze-like environments. The game supports multiple maps, character selection, and complex AI combat systems, featuring the following core functionalities:
- **Multiple Character Selection**: Players can choose different colored characters (blue/green/yellow/purple) to play.
- **Dynamic Map System**: Built-in maps with destructible walls (gmap1-6) supporting obstacle interactions.
- **Item System**: Over 10 item effects including health recovery, explosion range expansion, and remote bombs.
- **AI Enemy System**: Intelligent enemies using A* algorithm to actively pursue players and plan paths.
- **State Management**: Game flow control via state machine (main menu/settings/game/end).

---
## Game tutorial
### Selection interface
Put the mouse on the character and click the left button to become the locked state, and double-click to become the unlocked state. Only when the locked state is locked can you enter the select map interface.
### Select the map interface
You can select a map from the list on the left, a thumbnail of the map is on the right, and the arrow in the map is the player's birthplace.
### Game operation
- *Movement operation*: **w: Move up; s: move down; a: Move like left; d: move to the right**
- *Bomb placement operation*: **Press j to place the bomb. If there is a remote control bomb, press j for a short time to place it, and press j for a long time to detonate it.**
### Prop description
- *Heart*: **Add a maximum health**
- *Bombs*: **Add a maximum number of bombs**
- *Gloves*:**Add a grid explosion range**
- *Shield*:**Invincible for 5 seconds**
- *Remote control*: **Turn your bomb into a remote control bomb, the quantity is your maximum number of bombs, and it will become an ordinary bomb when you run out.**

---

### Environment Requirements
- Python 3.8+
- Pygame 2.1+
- Pygame_gui 0.9.54+