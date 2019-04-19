from django.contrib import admin


class BaseOwnerAdmin:
    '''
    1...
    2....
    '''
    exclude = ('owner',)

    # def save_model(self, request, obj, form, change):
    #     obj.owner = request.user
    #     return super(BaseOwnerAdmin, self).save_model(request, obj, form, change)
    def save_models(self):
        self.new_obj.owner = self.request.user
        return super().save_models()

    # def get_queryset(self, request):
    def get_list_queryset(self):
        qs = super().get_list_queryset()
        return qs.filter(owner=self.request.user)

