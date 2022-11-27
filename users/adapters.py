from allauth.account.adapter import DefaultAccountAdapter
from django.conf import settings

class CustomAccountAdapter(DefaultAccountAdapter): # dj-rest-auth 커스텀

        # 기본 저장 필드: first_name, last_name, username, email
        # 추가 저장 필드: profile_image
    def save_user(self, request, user, form, commit=False):
        user = super().save_user(request, user, form, commit)
        data = form.cleaned_data
        user.nickname = data.get("nickname")
        user.name = data.get("name")
        user.save()
        return user
    
    # def send_mail(self, template_prefix, email, context):
    #     context['activate_url'] = settings.URL_FRONT + \
    #         'verify-email/' + context['key']
    #     msg = self.render_mail(template_prefix, email, context)
    #     msg.send()

