"""Single source of truth for the 30-question knowledge-administrator bank.

ALL content is fictional: entries, enterprises, people, amounts and SOP names.
No real personal/enterprise data; no client name; no overseas SDK.
Eight required fields per question:
  question_id, type, stem, options, answer, explanation, knowledge_point, difficulty
Scenario questions additionally carry scenario_category + source_material.
"""
from __future__ import annotations

# Fictional SOP references cited in explanations.
SOP_ENTRY = "《知识条目入场标准（虚构 v1.0）》"
SOP_VIS = "《可见范围设定指引（虚构 v1.0）》"
SOP_SENS = "《敏感信息分级清单（虚构 v1.0）》"
SOP_EXPIRE = "《条目过期复核办法（虚构 v1.0）》"
SOP_SOPCHANGE = "《SOP 变更管理规范（虚构 v1.0）》"
SOP_BANK = "《题库上线审定规则（虚构 v1.0）》"
SOP_EXTRACT = "《萃取输出复核规程（虚构 v1.0）》"


def opt(*items):
    return [{"key": k, "text": t} for k, t in items]


QUESTIONS: list[dict] = [
    # ==================== 8 SINGLE CHOICE ====================
    {
        "question_id": "Q001", "type": "single_choice",
        "stem": f"依据{SOP_ENTRY}，知识条目入库前必须满足的条件是？",
        "options": opt(
            ("A", "条目必须由 AI 自动生成，因为人工撰写难以保证格式统一"),
            ("B", "条目须有可追溯来源与明确负责人"),
            ("C", "条目篇幅必须超过 500 字，短条目一律视为不完整而拒绝入场"),
            ("D", "条目必须一律对全体成员可见，否则就无法体现知识共享的价值"),
        ),
        "answer": "B",
        "explanation": (
            f"B 正确：{SOP_ENTRY}第 2 条要求「来源可追溯、责任人明确」，这是入场的硬门槛。"
            "A 错：AI 生成是可选的录入方式，不是准入条件；C 错：标准要求的是信息完整，"
            "没有 500 字的篇幅下限；D 错：可见范围按信息分类决定，不是一律全员——"
            "把敏感条目设为全员恰是典型违规（参见可见范围判定知识点）。"
        ),
        "knowledge_point": "入场质量标准", "difficulty": "easy",
    },
    {
        "question_id": "Q002", "type": "single_choice",
        "stem": "一份「会员企业融资意向汇总」条目含多家会员企业的融资金额与估值。依可见范围规则应如何设置？",
        "options": opt(
            ("A", "全体成员可见"),
            ("B", "仅指定角色（投资对接专员）可见"),
            ("C", "完全公开到平台官网，便于外部合作方直接检索对接"),
            ("D", "无需单独设置，默认继承成员企业自身的可见范围即可"),
        ),
        "answer": "B",
        "explanation": (
            f"B 正确：{SOP_VIS}规定敏感经营信息按「岗位角色」授权，投资对接专员属业务必需角色。"
            "A、C 错：融资计划属敏感信息，全员或公开是过度授权，正是本知识点的核心陷阱；"
            "D 错：条目不得默认继承可见范围，须显式判定。注意本题不是「指定个人」场景——"
            "汇总信息面向一类岗位，故角色授权而非单人授权。"
        ),
        "knowledge_point": "可见范围判定", "difficulty": "medium",
    },
    {
        "question_id": "Q003", "type": "single_choice",
        "stem": "下列哪一项最可能属于「未披露合作信息」，按敏感信息规则不得直接入库？",
        "options": opt(
            ("A", "已公开发布的活动议程，因此在任何情况下都无需再做可见性判定"),
            ("B", "会员企业在内部沟通中提及、尚未官宣的战略合作"),
            ("C", "通用的行业术语解释，因此默认属于对全员公开无害的内容"),
            ("D", "虚构嘉宾的公开头衔，虽然已公开但仍须逐条限制为指定个人可见"),
        ),
        "answer": "B",
        "explanation": (
            f"B 正确：{SOP_SENS}将「尚未对外官宣的合作关系」列为未披露合作信息，属敏感项，"
            "入库前须确认披露状态并限制可见范围。A、C、D 均为已公开或非敏感内容，"
            "不触发该规则。判据是「是否已对外披露」，而非内容是否有价值。"
        ),
        "knowledge_point": "敏感信息识别", "difficulty": "easy",
    },
    {
        "question_id": "Q004", "type": "single_choice",
        "stem": "为知识条目设置「过期复核」的主要目的是？",
        "options": opt(
            ("A", "尽快增加条目数量，使知识库覆盖更多主题以提升考核指标"),
            ("B", "定期确认内容仍准确有效，避免过时信息误导使用者"),
            ("C", "让所有条目在复核后自动转为私有可见，从而杜绝一切泄露可能"),
            ("D", "彻底免除人工审核工作，把过期判定与内容更新全部交给系统自动完成"),
        ),
        "answer": "B",
        "explanation": (
            f"B 正确：{SOP_EXPIRE}规定过期复核用于周期性验证内容时效性与准确性。"
            "A 错：复核与数量目标无关；C 错：复核不改变可见范围，只更新有效性判断；"
            "D 错：复核本身由人工执行，不能免除审核，反而强化审核。"
        ),
        "knowledge_point": "过期复核", "difficulty": "easy",
    },
    {
        "question_id": "Q005", "type": "single_choice",
        "stem": "某 SOP 仅修正一个错别字和一处排版，不改变流程步骤与审批权限。应如何判定？",
        "options": opt(
            ("A", "重大修订，须重新组织全员培训并更新全部岗位的操作手册"),
            ("B", "小幅修订，记录变更日志即可"),
            ("C", "须作废该 SOP 并重新立项编号，不能沿用原版本号继续发布"),
            ("D", "须升级为新的 SOP 编号并单独归档，原编号立即停止使用"),
        ),
        "answer": "B",
        "explanation": (
            f"B 正确：{SOP_SOPCHANGE}规定「不影响流程步骤、角色权限与审批链的编辑」为小幅修订，"
            "记录变更日志即可。A、C、D 错：三者都把非实质性编辑当作结构性变更，"
            "会造成不必要的培训成本与编号混乱。判据是「是否改变流程或权限」。"
        ),
        "knowledge_point": "SOP修订判定", "difficulty": "medium",
    },
    {
        "question_id": "Q006", "type": "single_choice",
        "stem": "某 SOP 将审批权限由「运营主管」改为「会员企业自行确认」，并新增两个流程步骤。应如何判定？",
        "options": opt(
            ("A", "小幅修订，仅在会议口头说明即可，不必留下变更记录"),
            ("B", "重大修订，须重新审定与培训"),
            ("C", "无需任何处理，审批人变更属于正常人事调整不影响文档效力"),
            ("D", "仅更新文档标题即可，无需通知相关岗位或更新培训材料"),
        ),
        "answer": "B",
        "explanation": (
            f"B 正确：{SOP_SOPCHANGE}规定凡改变审批权限归属或流程步骤的变更为重大修订，"
            "须重新审定、版本升级并组织培训。A 错：权限与步骤均变，不是小幅；"
            "C、D 错：重大变更必须走完整复审流程，不能以不处理或改标题代替。"
            "与 Q005 对照，可见判据是「流程/权限是否实质改变」。"
        ),
        "knowledge_point": "SOP修订判定", "difficulty": "medium",
    },
    {
        "question_id": "Q007", "type": "single_choice",
        "stem": f"一道 AI 生成的题目未标注来源依据，无法追溯出处。依{SOP_BANK}应如何处理？",
        "options": opt(
            ("A", "直接上线以扩充题库"),
            ("B", "退回补充来源，暂不上线"),
            ("C", "改成判断题即可上线"),
            ("D", "只要答案看起来合理便可上线"),
        ),
        "answer": "B",
        "explanation": (
            f"B 正确：{SOP_BANK}要求上线题目必须有可追溯来源，缺来源即退回补充。"
            "A、D 错：无来源的题目无法核对事实，答案「看起来合理」不构成审定依据；"
            "C 错：改变题型不解决来源缺失问题，属于绕过审定。"
        ),
        "knowledge_point": "题库审定", "difficulty": "medium",
    },
    {
        "question_id": "Q008", "type": "single_choice",
        "stem": "萃取 Agent 从虚构会议纪要生成的 FAQ 草稿中，将「参会 30 人」写成「参会 300 人」。复核时应？",
        "options": opt(
            ("A", "直接发布，AI 输出无需核对"),
            ("B", "标记为事实错误，退回修正后再审"),
            ("C", "忽略，数字差异不影响业务"),
            ("D", "由 AI 自动推算正确人数后发布"),
        ),
        "answer": "B",
        "explanation": (
            f"B 正确：{SOP_EXTRACT}要求人工核对 AI 抽取内容的事实一致性，数字失真须标记退回。"
            "A 错：AI 输出必须进复核队列，不得直接发布；C 错：人数失真属事实错误；"
            "D 错：AI 不负责计算或推算数值，须以原始材料为准由人工校正。"
        ),
        "knowledge_point": "萃取复核", "difficulty": "hard",
    },

    # ==================== 6 MULTIPLE CHOICE ====================
    {
        "question_id": "Q009", "type": "multiple_choice",
        "stem": "下列哪些属于敏感信息，需要限制可见范围或不得直接入库？（多选）",
        "options": opt(
            ("A", "会员企业的融资计划与估值"),
            ("B", "联系人的个人手机号与私人邮箱"),
            ("C", "尚未官宣的合作关系"),
            ("D", "已公开发布的行业白皮书，因含有行业汇总数据也应一律按敏感信息限制可见"),
        ),
        "answer": "A,B,C",
        "explanation": (
            f"A、B、C 正确：{SOP_SENS}分别将融资计划、个人联系方式、未披露合作列为敏感信息，"
            "须限制可见或暂缓入库。D 错：已公开白皮书不构成敏感信息。"
            "本题判据是「未公开 + 可识别到具体主体」，三项均符合。"
        ),
        "knowledge_point": "敏感信息识别", "difficulty": "medium",
    },
    {
        "question_id": "Q010", "type": "multiple_choice",
        "stem": "判定一条内部条目应设为「全员 / 指定角色 / 指定个人」时，需综合考虑哪些维度？（多选）",
        "options": opt(
            ("A", "信息分类等级"),
            ("B", "岗位角色的业务必要性"),
            ("C", "部门归属与知悉范围"),
            ("D", "条目标题的字数，标题过长的条目必须收窄为指定个人可见"),
        ),
        "answer": "A,B,C",
        "explanation": (
            f"A、B、C 正确：{SOP_VIS}规定可见范围判定采用「分类—角色—部门」三维度核对法，"
            "任一维度指向更严格的授权时取更严格者。D 错：标题字数与授权无关，是明显干扰项。"
            "将过度开放的设置（如把受限条目设全员）作为陷阱排除。"
        ),
        "knowledge_point": "可见范围判定", "difficulty": "medium",
    },
    {
        "question_id": "Q011", "type": "multiple_choice",
        "stem": "一道 AI 生成题目满足哪些条件方可上线？（多选）",
        "options": opt(
            ("A", "具有可追溯的来源依据"),
            ("B", "答案唯一、无歧义"),
            ("C", "不泄露敏感信息"),
            ("D", "题干篇幅足够长，只要题目写得详尽就可以豁免来源与唯一答案要求"),
        ),
        "answer": "A,B,C",
        "explanation": (
            f"A、B、C 正确：{SOP_BANK}规定上线三要件为「有来源、答案唯一、无敏感泄露」，"
            "缺一即退回。D 错：篇幅不是审定标准，长题干同样可能因非唯一答案被退回。"
            "三要件是并列必要条件，不能用其中一项替代另一项。"
        ),
        "knowledge_point": "题库审定", "difficulty": "medium",
    },
    {
        "question_id": "Q012", "type": "multiple_choice",
        "stem": "关于萃取 Agent 的输出，下列哪些说法符合规定？（多选）",
        "options": opt(
            ("A", "输出须进入人工复核队列"),
            ("B", "复核前不得直接对外发送"),
            ("C", "AI 不负责计算或推算金额"),
            ("D", "复核通过前可先向外部预览发布"),
        ),
        "answer": "A,B,C",
        "explanation": (
            f"A、B、C 正确：{SOP_EXTRACT}规定 AI 输出「先入队、后复核、不直发」，且 AI 不计算金额。"
            "D 错：预览发布同样属于对外发送，违反「不直发」红线——本题陷阱在于把预览"
            "包装成内部动作，实质上仍是对外披露。"
        ),
        "knowledge_point": "萃取复核", "difficulty": "hard",
    },
    {
        "question_id": "Q013", "type": "multiple_choice",
        "stem": "一条合格的知识条目应具备哪些特征？（多选）",
        "options": opt(
            ("A", "来源可追溯"),
            ("B", "内容准确、无明显事实错误"),
            ("C", "有明确的维护负责人"),
            ("D", "篇幅越短越好，任何超过两句话的条目都应视为冗长而退回"),
        ),
        "answer": "A,B,C",
        "explanation": (
            f"A、B、C 正确：{SOP_ENTRY}要求条目具备来源、准确性与责任人三项基本质量属性。"
            "D 错：标准强调信息完整，篇幅长短不构成质量判据，过短反而可能丢失关键条件。"
        ),
        "knowledge_point": "入场质量标准", "difficulty": "easy",
    },
    {
        "question_id": "Q014", "type": "multiple_choice",
        "stem": "哪些情况应触发知识条目的过期复核？（多选）",
        "options": opt(
            ("A", "达到预设的有效期"),
            ("B", "条目所引用的政策或规则发生变化"),
            ("C", "使用者反馈内容可能有误"),
            ("D", "条目的浏览次数上升，说明内容可能过时须立即触发过期复核"),
        ),
        "answer": "A,B,C",
        "explanation": (
            f"A、B、C 正确：{SOP_EXPIRE}规定到期、依据变更、用户纠错反馈均为复核触发条件。"
            "D 错：浏览量上升只反映关注度，不说明内容时效性变化，不构成复核触发条件。"
        ),
        "knowledge_point": "过期复核", "difficulty": "medium",
    },

    # ==================== 4 TRUE / FALSE ====================
    {
        "question_id": "Q015", "type": "true_false",
        "stem": "涉及会员企业融资计划的条目，默认应对全体成员开放以促进资源对接。",
        "options": opt(("A", "正确"), ("B", "错误")),
        "answer": "B",
        "explanation": (
            f"B 正确（陈述错误）。A 错：{SOP_SENS}将融资计划列为敏感信息，"
            f"{SOP_VIS}要求按角色最小化授权，默认全员开放属过度授权。"
            "「促进资源对接」不能作为绕过敏感信息管控的理由，正确做法是通过投资对接角色定向授权。"
        ),
        "knowledge_point": "可见范围判定", "difficulty": "easy",
    },
    {
        "question_id": "Q016", "type": "true_false",
        "stem": "萃取 Agent 生成的 FAQ 草稿，只要语句通顺即可直接进入正式知识库。",
        "options": opt(("A", "正确"), ("B", "错误")),
        "answer": "B",
        "explanation": (
            f"B 正确（陈述错误）。A 错：{SOP_EXTRACT}明确 AI 输出必须进入复核队列，"
            "人工核对事实准确性与敏感信息后方可入库。语句通顺只涉及表达层，"
            "无法发现数字失真或敏感泄露，不能替代内容复核。"
        ),
        "knowledge_point": "萃取复核", "difficulty": "medium",
    },
    {
        "question_id": "Q017", "type": "true_false",
        "stem": "仅修改错别字、不改变流程步骤与权限的 SOP 变更，通常判定为小幅修订。",
        "options": opt(("A", "正确"), ("B", "错误")),
        "answer": "A",
        "explanation": (
            f"A 正确（陈述正确）。B 错：{SOP_SOPCHANGE}以「是否改变流程步骤、角色权限与审批链」"
            "作为大小修订的分界；纯文字与排版修正不改变执行逻辑，属小幅修订，记录变更日志即可。"
        ),
        "knowledge_point": "SOP修订判定", "difficulty": "easy",
    },
    {
        "question_id": "Q018", "type": "true_false",
        "stem": "AI 萃取时若发现金额数字前后不一致，可自行计算并填入其认为正确的值。",
        "options": opt(("A", "正确"), ("B", "错误")),
        "answer": "B",
        "explanation": (
            f"B 正确（陈述错误）。A 错：{SOP_EXTRACT}规定 AI 不计算金额，"
            "数字不一致须标记并退回人工核对原始材料。AI 自行推算会引入无法追溯的数值，"
            "违反来源可追溯原则，是红线行为。"
        ),
        "knowledge_point": "萃取复核", "difficulty": "medium",
    },
]
