from enum import Enum


class RenewalFormUralV3(Enum):
    URAL_RENEWAL_EFD_BEGINNING = "UralRenewalEfdBeginning"
    URAL_RENEWAL_EFD_PRICELIST = "UralRenewalEfdPriceList"
    URAL_RENEWAL_EFD_OFFER = "UralRenewalEfdOffer"
    URAL_RENEWAL_EFD_CLIENT = "UralRenewalEfdClient"
    URAL_RENEWAL_EFD_EMAIL_CONFIRM = "UralRenewalEfdEmailConfirm"
    URAL_RENEWAL_EFD_ADDRESS = "UralRenewalEfdAddress"
    URAL_RENEWAL_EFD_DELEVERY = "UralRenewalEfdDelivery"
    URAL_RENEWAL_EFD_WAITING = "UralRenewalEfdWaiting"
    URAL_RENEWAL_EFD_PDF_PREVIEW = "UralRenewalEfdPdfPreview"
    URAL_RENEWAL_EFD_GENERATE_ERROR = "UralRenewalEfdGenerateError"
    URAL_RENEWAL_EFD_SIGNATURE = "UralRenewalEfdSignature"
    URAL_RENEWAL_EFD_COMPLETE = "UralRenewalEfdComplete"
