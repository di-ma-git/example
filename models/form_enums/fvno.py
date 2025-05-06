from enum import Enum


class FvnoForm(Enum):
    FVNO_BEGINNING = "FVNOBeginning"
    FVNO_OFFER = "FVNOOffer"
    FVNO_CLIENT = "'FVNOClient"
    FVNO_EMAIL_CONFIRM = "FVNOEmailConfirm"
    FVNO_ADDRESS = "FVNOAddress"
    FVNO_TEXT_PREVIEW = "FVNOTextPreview"
    FVNO_EQUIPMENT = "FVNOEquipment"
    FVNO_GENERATE_ERROR = "FVNOGenerateError"
    FVNO_WAITING = "FVNOWaiting"
    FVNO_PDF_PREVIEW = "FVNOPdfPreview"
    FVNO_EMPLOYEE_CONFIRM = "FVNOEmployeeConfirm"
    FVNO_SIGNATURE = "FVNOSignature"
    FVNO_COMPLETE = "FVNOComplete"
