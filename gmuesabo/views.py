from django.utils.translation import gettext_lazy as _

from juntagrico.config import Config
from juntagrico.entity.subs import Subscription
from juntagrico.views.manage import SubscriptionView


class SubscriptionSharesView(SubscriptionView):
    permission_required = [
        ['juntagrico.view_subscription', 'juntagrico.change_subscription', 'juntagrico.can_filter_subscriptions'],
        ['juntagrico.view_share', 'juntagrico.change_share',]
    ]
    template_name = 'manage/subscription/shares.html'
    queryset = Subscription.objects.active
    title = _('{subscriptions} und {shares}').format(
        subscriptions=Config.vocabulary('subscription_pl'),
        shares=Config.vocabulary('share_pl')
    )
