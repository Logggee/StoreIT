from enum import Enum, auto

class Storage_Page_State(Enum):
    INIT = auto()
    ADD_ITEM_FORM_ERROR = auto()
    ADD_EXISTING_ITEM_FORM_ERROR = auto()
    DESTORE_ITEM_FORM_ERROR = auto()
    STORE_ITEM_PROCESS = auto()
    DESTORE_ITEM_PROCESS = auto()