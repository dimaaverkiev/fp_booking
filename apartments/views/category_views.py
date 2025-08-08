from rest_framework.generics import ListCreateAPIView, RetrieveUpdateDestroyAPIView
from rest_framework.permissions import IsAdminUser
from apartments.models import Category
from apartments.serializers.category_serializers import ListCategorySerializer, CreateUpdateCategorySerializer




class CreateFederalStateListView(ListCreateAPIView):
    permission_classes = [IsAdminUser]

    queryset = Category.objects.all()

    def get_serializer_class(self):
        if self.request.method == 'GET':
            return ListCategorySerializer
        return CreateUpdateCategorySerializer




class UpdateFederalStateListView(RetrieveUpdateDestroyAPIView):
    permission_classes = [IsAdminUser]
    queryset = Category.objects.all()

    def get_serializer_class(self):
        if self.request.method == 'GET':
            return ListCategorySerializer
        return CreateUpdateCategorySerializer