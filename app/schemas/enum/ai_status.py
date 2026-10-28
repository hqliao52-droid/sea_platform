from enum import Enum

class AIStatus(Enum):
    """AI 状态枚举"""

    ANALYZING = "analyzing"
    RETRIEVING = "retrieving"
    GENERATING = "generating"
    READING = "reading"
    DONE = "done"
    EXCEPTION = "exception"
    END = "end"

class MsgType(Enum):
    USER = 1
    ASSISTANT = 2
    SYSTEM = 3
    TOOLS = 4
    SKILL = 5
    MCP = 6

class Role(Enum):
    USER = "user"
    ASSISTANT = "assistant"
    SYSTEM = "system"
    TOOLS = "tools"

ROLE_FORMAT: dict[Role, tuple[MsgType, ]] = {
    Role.USER: (MsgType.USER,),
    Role.ASSISTANT: (MsgType.ASSISTANT,),
    Role.SYSTEM: (MsgType.SYSTEM,),
    Role.TOOLS: (MsgType.TOOLS,),
}

