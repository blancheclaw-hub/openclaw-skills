---
name: project-atom
description: 项目原子管理系统 - 根据项目复杂度自动评估并组合角色原子
user-invocable: true
metadata:
  {"openclaw": {"requires": {"bins": [], "env": {}}, "always": false}}
---

# SKILL.md - 项目原子管理系统

> 根据项目复杂度自动评估并组合角色原子的 SKILL

## 基本信息

- **名称**: project-atom
- **版本**: 1.0.0
- **作者**: BlancheWong & BlancheClaw
- **创建日期**: 2026-03-17

## 描述

项目原子组合管理系统，用于根据项目复杂度自动评估并组合合适的角色原子。

核心功能：
- 复杂度评估（基于任务数、风险评分、历史返工率）
- 原子组合（简单项目聚合，复杂项目拆分）
- 角色配置推荐

## 触发关键词

- 项目复杂度
- 角色组合
- 原子组合
- 虚拟部门
- project-atom

## 触发场景

当用户提出以下问题时自动触发：
- "评估这个项目的复杂度"
- "帮我组合原子角色"
- "创建简单/中等/复杂项目的角色方案"
- "这个项目应该用什么角色"

## 功能模块

### 1. evaluate_complexity

评估项目复杂度

**输入参数**：
- `task_count` (number): 任务数量
- `risk_score` (number): 风险评分 (0-1)
- `rework_rate` (number): 历史返工率 (0-1)

**输出**：
- 复杂度等级: simple | medium | complex
- 评估理由

### 2. compose_atoms

根据复杂度组合原子

**输入参数**：
- `complexity` (string): 复杂度等级

**输出**：
- 角色名称
- 原子组合列表
- 核心职责描述
- 标准化输出产物

### 3. generate_report

生成完整的项目角色方案报告

**输入参数**：
- `project_info` (object): 项目信息

**输出**：
- 完整的项目角色配置方案（Markdown格式）

## 配置文件

| 文件 | 用途 |
|------|------|
| `config/complexity_rules.yaml` | 复杂度判断规则 |
| `config/atom_templates.yaml` | 原子组合模板 |
| `config/skills_inventory.yaml` | 技能标签库（可选） |

## 使用示例

### 示例1：简单项目评估
```
用户：项目有3个任务，风险0.2，历史返工率5%

输出：
- 复杂度：简单 (simple)
- 推荐角色：全栈执行者
- 原子组合：Ql + A + L + Vt + D + O
- 核心职责：单人完成全流程
```

### 示例2：复杂项目评估
```
用户：项目有20个任务，风险0.7，历史返工率15%

输出：
- 复杂度：复杂 (complex)
- 推荐角色：
  - 项目质检官：Qa + Qp + Vt + Ki
  - 模块开发工程师：A + L + Ki
  - 开源交付专员：D + Ki
```

## 更新日志

- 2026-03-17 v1.0.0 初始版本

---

*本 SKILL 由 BlancheWong 提出需求，BlancheClaw 开发实现*
-e 

## 安全 gating

- 用户授权操作
- 数据隔离
- 敏感信息保护
