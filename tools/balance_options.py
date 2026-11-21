"""One-off authoring helper: expand WRONG options so they are length-comparable
to the correct option (kills the 'pick the longest answer' shortcut).

Applies to source files via exact-string replacement; each replacement keeps the
option WRONG and plausible (adds a reasonable-sounding but incorrect rationale).
Run once, then verify with tools/validate.py. Idempotent: skips if already expanded.
"""
from __future__ import annotations

from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]

# (source_file, old_option_text_fragment, new_full_option_text)
EDITS: list[tuple[str, str, str]] = [
    # ---------- single choice ----------
    ("questions_data.py", "条目必须由 AI 自动生成",
     "条目必须由 AI 自动生成，因为人工撰写难以保证格式统一"),
    ("questions_data.py", "条目篇幅必须超过 500 字",
     "条目篇幅必须超过 500 字，短条目一律视为不完整而拒绝入场"),
    ("questions_data.py", "条目必须一律对全体成员可见",
     "条目必须一律对全体成员可见，否则就无法体现知识共享的价值"),
    ("questions_data.py", "完全公开，便于资源对接",
     "完全公开到平台官网，便于外部合作方直接检索对接"),
    ("questions_data.py", "无需设置，默认继承",
     "无需单独设置，默认继承成员企业自身的可见范围即可"),
    ("questions_data.py", "已公开发布的活动议程",
     "已公开发布的活动议程，因此在任何情况下都无需再做可见性判定"),
    ("questions_data.py", "通用的行业术语解释",
     "通用的行业术语解释，因此默认属于对全员公开无害的内容"),
    ("questions_data.py", "虚构嘉宾的公开头衔",
     "虚构嘉宾的公开头衔，虽然已公开但仍须逐条限制为指定个人可见"),
    ("questions_data.py", "尽快增加条目数量",
     "尽快增加条目数量，使知识库覆盖更多主题以提升考核指标"),
    ("questions_data.py", "让所有条目自动转为私有可见",
     "让所有条目在复核后自动转为私有可见，从而杜绝一切泄露可能"),
    ("questions_data.py", "彻底免除人工审核工作",
     "彻底免除人工审核工作，把过期判定与内容更新全部交给系统自动完成"),
    ("questions_data.py", "重大修订，须重新全员培训",
     "重大修订，须重新组织全员培训并更新全部岗位的操作手册"),
    ("questions_data.py", "须作废该 SOP 并重建",
     "须作废该 SOP 并重新立项编号，不能沿用原版本号继续发布"),
    ("questions_data.py", "须升级为新的 SOP 编号",
     "须升级为新的 SOP 编号并单独归档，原编号立即停止使用"),
    ("questions_data.py", "小幅修订，记录即可",
     "小幅修订，仅在会议口头说明即可，不必留下变更记录"),
    ("questions_data.py", "无需任何处理",
     "无需任何处理，审批人变更属于正常人事调整不影响文档效力"),
    ("questions_data.py", "仅更新文档标题即可",
     "仅更新文档标题即可，无需通知相关岗位或更新培训材料"),
]

# ---------- multi choice (expand single short D distractors) ----------
EDITS += [
    ("questions_data.py", "已公开发布的行业白皮书",
     "已公开发布的行业白皮书，因含有行业汇总数据也应一律按敏感信息限制可见"),
    ("questions_data.py", "条目标题的字数",
     "条目标题的字数，标题过长的条目必须收窄为指定个人可见"),
    ("questions_data.py", "题干篇幅足够长",
     "题干篇幅足够长，只要题目写得详尽就可以豁免来源与唯一答案要求"),
    ("questions_data.py", "篇幅越短越好",
     "篇幅越短越好，任何超过两句话的条目都应视为冗长而退回"),
    ("questions_data.py", "条目的浏览次数上升",
     "条目的浏览次数上升，说明内容可能过时须立即触发过期复核"),
]

# ---------- scenario questions ----------
EDITS += [
    ("scenarios_data.py", "全体成员可见，读书会属公开活动",
     "全体成员可见，读书会报名通知已群发，故回执汇总也可一并全员公开"),
    ("scenarios_data.py", "完全公开，便于宣传",
     "完全公开到官网宣传栏，把参会企业联系人职务作为成果展示"),
    ("scenarios_data.py", "无需设置，默认继承",
     "无需单独设置，默认继承上一年度同类读书会条目的可见范围"),
    ("scenarios_data.py", "没有问题，可直接入库",
     "没有问题，可直接入库，只要姓名是化名则手机号与邮箱无须脱敏"),
    ("scenarios_data.py", "问题在于篇幅过短",
     "问题在于篇幅过短，应该补充更多会议背景后再直接对外发布"),
    ("scenarios_data.py", "只要把姓名删掉即可",
     "只要把姓名删掉即可，手机号与邮箱本身不构成需要保护的个人信息"),
    ("scenarios_data.py", "保持现状，规则一旦发布即长期有效",
     "保持现状，规则一旦发布即长期有效，不必设置任何复核日期也不核对版本"),
    ("scenarios_data.py", "直接删除全部积分内容",
     "直接删除全部积分内容，凡依据旧版本的条目都应清库而非复核更新"),
    ("scenarios_data.py", "把可见范围改为全员即可",
     "把可见范围改为全员即可，让所有成员共同判断规则是否仍然有效"),
    ("scenarios_data.py", "重大修订，须重新审定与全员培训",
     "重大修订，须重新审定并组织全员培训且同步更新岗位操作手册"),
    ("scenarios_data.py", "须作废并重建整份 SOP",
     "须作废并重建整份 SOP，原变更单作废并从 v1.0 重新编号发布"),
    ("scenarios_data.py", "须变更 SOP 编号",
     "须变更 SOP 编号并另起文档，原编号立即停用不再保留历史版本"),
    ("scenarios_data.py", "直接入库，内容方向正确即可",
     "直接入库，内容方向正确即可，来源与负责人可在后续季度统一补齐"),
    ("scenarios_data.py", "先入库，之后再补信息",
     "先入库对外提供服务，之后再按季度批量补充来源、负责人与版本信息"),
    ("scenarios_data.py", "改为判断题格式后入库",
     "改为判断题格式后入库，换一种题型即可跳过来源与负责人校验"),
    ("scenarios_data.py", "仅指定个人可见",
     "仅指定个人可见，把已公开的年会议程只授权给运营负责人一人查看"),
    ("scenarios_data.py", "仅管理层可见",
     "仅管理层可见，公开议程也须先经管理层审批后才能对普通成员开放"),
    ("scenarios_data.py", "不设置任何可见范围",
     "不设置任何可见范围，让系统按默认值处理即可不必显式声明"),
    ("scenarios_data.py", "可以上线，题干清晰",
     "可以上线，题干清晰即可，来源栏留空只是格式问题不影响作答"),
    ("scenarios_data.py", "可以上线，只要把答案设为 B",
     "可以上线，只要把标准答案设为 B，其余近似选项自动成为干扰项"),
    ("scenarios_data.py", "改为判断题即可上线",
     "改为判断题即可上线，换题型后原来源缺失与答案非唯一问题自动消失"),
    ("scenarios_data.py", "可以上线，两要件已满足",
     "可以上线，两要件已满足，解析中的金额只是举例无需按敏感信息处理"),
    ("scenarios_data.py", "可以上线，但把来源栏加密",
     "可以上线，但把来源栏加密保存，解析中的融资金额仍可按原样对外展示"),
    ("scenarios_data.py", "改为多选题即可上线",
     "改为多选题即可上线，只要把泄露句改为多选干扰项就不再构成敏感信息"),
    ("scenarios_data.py", "直接发布，AI 已完整抽取",
     "直接发布，AI 已完整抽取且与原文结构一致，数字差异不影响理解"),
    ("scenarios_data.py", "忽略该数字，保留其余内容发布",
     "忽略该数字并保留其余内容发布，出席人数属于细节不影响 FAQ 的价值"),
    ("scenarios_data.py", "由 AI 自动重新计算出席人数",
     "由 AI 自动重新计算出席人数并回填，无需人工再核对会议纪要原文"),
    ("scenarios_data.py", "可以发布，内容忠于原文",
     "可以发布，内容忠于原文，尚未官宣的合作反正迟早会公开"),
    ("scenarios_data.py", "可以发布，因为已标注「虚构」",
     "可以发布，因为已标注「虚构」，虚构标记自动豁免一切敏感信息规则"),
    ("scenarios_data.py", "仅需把企业名称改为代号即可发布",
     "仅需把企业名称改为代号即可发布，未官宣事实本身不构成泄露"),
    ("scenarios_data.py", "可以上线，来源栏已填写",
     "可以上线，来源栏已填写即视为可核验，知识库中有无该版本不必深究"),
    ("scenarios_data.py", "可以上线，把来源改成 v2.0",
     "可以上线，把来源直接改成库内存在的 v2.0，答案沿用原草稿即可"),
    ("scenarios_data.py", "直接驳回且不再处理",
     "直接驳回该 AI 题且不再处理，也无须向出题方反馈驳回原因"),
    ("scenarios_data.py", "直接发布，加法结果正确",
     "直接发布，加法结果正确，原文注明待复核只是流程性表述不影响数字"),
    ("scenarios_data.py", "保留结果，改为「约 220 万元」即可发布",
     "保留结果，改为「约 220 万元」即可发布，模糊表述即可规避财务复核"),
    ("scenarios_data.py", "由 AI 再次核对后发布",
     "由 AI 再次核对加法后发布，第二次校验可替代财务人工复核"),
]


def main() -> None:
    for fname in ("questions_data.py", "scenarios_data.py"):
        path = ROOT / fname
        text = path.read_text(encoding="utf-8")
        changed = 0
        for _, old, new in [e for e in EDITS if e[0] == fname]:
            # replace only the option text literal (quoted string) occurrence
            needle = f'"{old}"'
            if needle in text:
                text = text.replace(needle, f'"{new}"')
                changed += 1
        path.write_text(text, encoding="utf-8")
        print(f"{fname}: applied {changed} edits")


if __name__ == "__main__":
    main()
