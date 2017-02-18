class UserRetriever:
    def __init__(self):
        import logging
        super().__init__()
        self.logger = logging.getLogger(__name__)

    def get_user_extra_info_if_exists(self, user):
        from pastebin.models import UserExtraInfo
        try:
            stats = UserExtraInfo.objects.get(user=user)
            return stats
        except UserExtraInfo.DoesNotExist:
            return None