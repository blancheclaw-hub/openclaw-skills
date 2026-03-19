#!/usr/bin/env python3
"""
项目原子管理系统 - 复杂度评估器
根据任务数、风险评分、历史返工率评估项目复杂度
纯 Python 实现，无外部依赖
"""

import json
import os
import sys

# 配置路径
SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
CONFIG_DIR = os.path.join(os.path.dirname(SCRIPT_DIR), 'config')
RULES_FILE = os.path.join(CONFIG_DIR, 'complexity_rules.json')


def load_rules():
    """加载复杂度规则配置"""
    with open(RULES_FILE, 'r', encoding='utf-8') as f:
        return json.load(f)


def evaluate_complexity(task_count: int, risk_score: float, rework_rate: float) -> dict:
    """
    评估项目复杂度
    
    Args:
        task_count: 任务数量
        risk_score: 风险评分 (0-1)
        rework_rate: 历史返工率 (0-1)
    
    Returns:
        dict: 复杂度评估结果
    """
    rules = load_rules()
    
    # 获取规则
    simple = rules.get('simple', {})
    medium = rules.get('medium', {})
    complex_rule = rules.get('complex', {})
    
    # 简单项目判断
    if (task_count <= simple.get('max_tasks', 5) and 
        risk_score <= simple.get('max_risk_score', 0.3) and 
        rework_rate <= simple.get('max_rework_rate', 0.1)):
        return {
            'complexity': 'simple',
            'level': '简单',
            'description': simple.get('description', ''),
            'reason': f'任务数{task_count}≤{simple.get("max_tasks")}, 风险{risk_score}≤{simple.get("max_risk_score")}, 返工率{rework_rate}≤{simple.get("max_rework_rate")}'
        }
    
    # 中等项目判断
    if (task_count >= medium.get('min_tasks', 6) and 
        task_count <= medium.get('max_tasks', 15) and 
        risk_score <= medium.get('max_risk_score', 0.6) and 
        rework_rate <= medium.get('max_rework_rate', 0.2)):
        return {
            'complexity': 'medium',
            'level': '中等',
            'description': medium.get('description', ''),
            'reason': f'任务数{task_count}在{medium.get("min_tasks")}-{medium.get("max_tasks")}之间, 风险{risk_score}≤{medium.get("max_risk_score")}'
        }
    
    # 复杂项目
    return {
        'complexity': 'complex',
        'level': '复杂',
        'description': complex_rule.get('description', ''),
        'reason': f'任务数{task_count}>{medium.get("max_tasks")}或风险{risk_score}>{medium.get("max_risk_score")}'
    }


def main():
    """命令行入口"""
    if len(sys.argv) >= 4:
        task_count = int(sys.argv[1])
        risk_score = float(sys.argv[2])
        rework_rate = float(sys.argv[3])
        
        result = evaluate_complexity(task_count, risk_score, rework_rate)
        print(f"复杂度: {result['level']} ({result['complexity']})")
        print(f"说明: {result['description']}")
        print(f"理由: {result['reason']}")
    else:
        # 测试示例
        print("=== 项目复杂度评估测试 ===\n")
        
        test_cases = [
            (3, 0.2, 0.05, "简单项目"),
            (10, 0.4, 0.1, "中等项目"),
            (20, 0.7, 0.15, "复杂项目")
        ]
        
        for task_count, risk, rework, desc in test_cases:
            result = evaluate_complexity(task_count, risk, rework)
            print(f"【{desc}】任务数={task_count}, 风险={risk}, 返工率={rework}")
            print(f"  → {result['level']} ({result['complexity']})")
            print(f"  → 理由: {result['reason']}\n")


if __name__ == '__main__':
    main()
