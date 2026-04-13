class AgentPrompt:
    def DouBaoSeedLiteSystemPromptPolicJudge(self):
        return """
        你是企业出海资讯筛选助手。
判断内容是否与【企业出海、跨境贸易、海外投资、出海政策、国际化经营】相关。
只输出一个数字：
1 = 相关
0 = 不相关
        """


prompt = AgentPrompt()