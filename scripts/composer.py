#!/usr/bin/env python3
"""
项目原子管理系统 - 原子组合器
根据复杂度等级组合合适的角色原子
纯 Python 实现，无外部依赖
"""

import json
import os
import sys

# 配置路径
SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
CONFIG_DIR = os.path.join(os.path.dirname(SCRIPT_DIR), 'config')
TEMPLATES_FILE = os.path.join(CONFIG_DIR, 'atom_templates.json')


def load_templates():
    """加载原子组合模板"""
    with open(TEMPLATES_FILE, 'r', encoding='utf-8') as f:
        return json.load(f)


def get_role_template(complexity: str) -> dict:
    """
    获取指定复杂度的角色模板
    
    Args:
        complexity: 复杂度等级 (simple/medium/complex)
    
    Returns:
        dict: 角色配置
    """
    templates = load_templates()
    
    mapping = {
        'simple': 'simple_project',
        'medium': 'medium_project', 
        'complex': 'complex_project'
    }
    
    template_key = mapping.get(complexity, 'simple_project')
    return templates.get(template_key, {})


def compose_atoms(complexity: str) -> dict:
    """
    根据复杂度组合原子
    
    Args:
        complexity: 复杂度等级
    
    Returns:
        dict: 原子组合结果
    """
    template = get_role_template(complexity)
    
    if not template:
        return {
            'success': False,
            'message': f'未找到复杂度为 {complexity} 的模板'
        }
    
    roles = template.get('roles', [])
    atom_meanings = template.get('atom_meanings', {})
    
    # 构建角色列表
    role_list = []
    for role in roles:
        role_info = {
            'name': role.get('name', ''),
            'atoms': role.get('atoms', []),
            'responsibilities': role.get('responsibilities', ''),
            'output': role.get('output', ''),
            'atom_details': [f"{atom}: {atom_meanings.get(atom, '')}" for atom in role.get('atoms', [])]
        }
        role_list.append(role_info)
    
    return {
        'success': True,
        'complexity': complexity,
        'role_count': len(roles),
        'roles': role_list
    }


def evaluate_complexity(task_count: int, risk_score: float, rework_rate: float) -> dict:
    """评估项目复杂度（简化版）"""
    if task_count <= 5 and risk_score <= 0.3 and rework_rate <= 0.1:
        return {'complexity': 'simple', 'level': '简单'}
    if task_count <= 15 and risk_score <= 0.6 and rework_rate <= 0.2:
        return {'complexity': 'medium', 'level': '中等'}
    return {'complexity': 'complex', 'level': '复杂'}


def generate_report(project_info: dict) -> str:
    """
    生成完整的项目角色方案报告
    
    Args:
        project_info: 项目信息，包含 task_count, risk_score, rework_rate
    
    Returns:
        str: Markdown 格式的报告
    """
    task_count = project_info.get('task_count', 0)
    risk_score = project_info.get('risk_score', 0)
    rework_rate = project_info.get('rework_rate', 0)
    
    complexity_result = evaluate_complexity(task_count, risk_score, rework_rate)
    complexity = complexity_result['complexity']
    
    # 获取原子组合
    atom_result = compose_atoms(complexity)
    
    # 生成报告
    report = f"""# 📋 项目角色方案报告

## 项目信息

| 参数 | 值 |
|------|-----|
| 任务数量 | {task_count} |
| 风险评分 | {risk_score} |
| 历史返工率 | {rework_rate} |

## 复杂度评估

- **复杂度等级**: {complexity_result['level']} ({complexity})

## 角色配置

"""
    
    for i, role in enumerate(atom_result['roles'], 1):
        report += f"""### {i}. {role['name']}

- **原子组合**: {' + '.join(role['atoms'])}
- **核心职责**: {role['responsibilities']}
- **输出产物**: {role['output']}

**原子说明**:
"""
        for atom_detail in role['atom_details']:
            report += f"- {atom_detail}\n"
        report += "\n"
    
    report += """---

*本报告由 project-atom SKILL 自动生成*
"""
    
    return report


def main():
    """命令行入口"""
    if len(sys.argv) >= 2:
        complexity = sys.argv[1]
        result = compose_atoms(complexity)
        
        if result['success']:
            print(f"复杂度: {result['complexity']}")
            print(f"角色数量: {result['role_count']}\n")
            
            for i, role in enumerate(result['roles'], 1):
                print(f"【{role['name']}】")
                print(f"  原子: {' + '.join(role['atoms'])}")
                print(f"  职责: {role['responsibilities']}")
                print(f"  输出: {role['output']}\n")
        else:
            print(f"错误: {result['message']}")
    else:
        # 测试示例
        print("=== 原子组合测试 ===\n")
        
        for complexity in ['simple', 'medium', 'complex']:
            result = compose_atoms(complexity)
            print(f"【{complexity}】 角色数: {result['role_count']}")
            for role in result['roles']:
                print(f"  - {role['name']}: {' + '.join(role['atoms'])}")
            print()


if __name__ == '__main__':
    main()
