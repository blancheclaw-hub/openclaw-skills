#!/usr/bin/env python3
"""
项目原子管理系统 - 技能匹配器
根据角色原子需求匹配合适的工程师
"""

import json
import os
import sys

# 配置路径
SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
CONFIG_DIR = os.path.join(os.path.dirname(SCRIPT_DIR), 'config')
SKILLS_FILE = os.path.join(CONFIG_DIR, 'skills_inventory.json')


def load_skills():
    """加载技能标签库"""
    with open(SKILLS_FILE, 'r', encoding='utf-8') as f:
        return json.load(f)


def match_skills(atom_requirements: list) -> list:
    """
    根据原子需求匹配工程师
    
    Args:
        atom_requirements: 原子列表，如 ["Qa", "Qp", "Vt"]
    
    Returns:
        list: 匹配的工程师列表（按匹配度排序）
    """
    data = load_skills()
    engineers = data.get('engineers', [])
    atom_skills = data.get('atom_skill_requirements', {})
    
    # 计算每个工程师的匹配度
    results = []
    for eng in engineers:
        score = 0
        matched_tags = []
        
        # 收集该工程师拥有的技能标签
        eng_tags = eng.get('tags', [])
        
        # 检查每个原子需求
        for atom in atom_requirements:
            required_skills = atom_skills.get(atom, [])
            if required_skills:
                for req_skill in required_skills:
                    if req_skill in eng_tags:
                        score += 1
                        matched_tags.append(req_skill)
        
        # 检查负载
        current_load = eng.get('current_load', 0)
        max_load = eng.get('max_load', 0.8)
        load_available = current_load < max_load
        
        # 负载因子：负载越低，分数越高（权重50%）
        load_factor = 1.0 - (current_load / max_load) if max_load > 0 else 0
        
        # 技能匹配分数（权重50%）
        skill_score = score / max(len(atom_requirements), 1)
        
        # 综合得分 = 技能匹配 * 0.5 + 负载可用 * 0.5
        final_score = (skill_score * 0.5 + load_factor * 0.5) * 100
        
        results.append({
            'id': eng.get('id'),
            'name': eng.get('name'),
            'score': round(final_score, 2),
            'skill_score': score,
            'matched_tags': matched_tags,
            'current_load': current_load,
            'available': load_available
        })
    
    # 按得分排序
    results.sort(key=lambda x: x['score'], reverse=True)
    
    return results


def recommend_engineers(roles: list) -> dict:
    """
    为所有角色推荐工程师
    
    Args:
        roles: 角色列表，每个包含 name 和 atoms
    
    Returns:
        dict: 每个角色推荐的工程师
    """
    recommendations = {}
    
    for role in roles:
        role_name = role.get('name', '')
        atoms = role.get('atoms', [])
        
        # 匹配工程师
        matches = match_skills(atoms)
        
        # 取前3名
        top_matches = [m for m in matches if m['available']][:3]
        
        recommendations[role_name] = top_matches
    
    return recommendations


def generate_skill_match_report(atom_result: dict, recommendations: dict) -> str:
    """
    生成技能匹配报告
    
    Args:
        atom_result: 原子组合结果
        recommendations: 技能匹配结果
    
    Returns:
        str: Markdown 格式的报告
    """
    report = """## 技能匹配推荐

"""
    
    for role_name, matches in recommendations.items():
        report += f"""### {role_name}

| 工程师 | 匹配度 | 当前负载 | 匹配技能 |
|--------|--------|----------|----------|
"""
        for m in matches:
            tags = ', '.join(m['matched_tags']) if m['matched_tags'] else '-'
            report += f"| {m['name']} | {m['score']} | {int(m['current_load']*100)}% | {tags} |\n"
        
        report += "\n"
    
    report += """---

*技能匹配基于技能标签匹配度 + 负载可用性综合计算*
"""
    
    return report


def main():
    """命令行入口"""
    if len(sys.argv) >= 2:
        atoms = sys.argv[1].split(',')
        results = match_skills(atoms)
        
        print(f"技能匹配结果 (原子: {atoms}):\n")
        for r in results[:3]:
            if r['available']:
                print(f"【{r['name']}】得分: {r['score']}, 负载: {int(r['current_load']*100)}%")
                print(f"  匹配技能: {', '.join(r['matched_tags'])}\n")
    else:
        # 测试示例
        print("=== 技能匹配测试 ===\n")
        
        test_cases = [
            (["Qa", "Qp", "Vt"], "项目质检官"),
            (["A", "L"], "模块开发工程师"),
            (["I", "T", "K"], "需求分析师")
        ]
        
        for atoms, role_name in test_cases:
            print(f"【{role_name}】需要原子: {atoms}")
            results = match_skills(atoms)
            for r in results[:3]:
                if r['available']:
                    print(f"  → {r['name']}: {r['score']}分, 负载{int(r['current_load']*100)}%")
            print()


if __name__ == '__main__':
    main()
