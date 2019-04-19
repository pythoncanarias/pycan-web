import logging
from datetime import timedelta

logger = logging.getLogger(__name__)


class MemberService():
    @staticmethod
    def renew_membership(member):
        new_membership_date = member.member_until
        member.member_until = new_membership_date + timedelta(days=365)
        member.save()
        logger.info(
            'Member %s renewed membership untill %s',
            member.id,
            new_membership_date,
        )

        return member
