from rest_framework.generics import ListCreateAPIView, RetrieveUpdateDestroyAPIView
from rest_framework.permissions import IsAdminUser
from apartments.models import FederalState
from apartments.serializers.federal_state_serializers import ListFederalStateSerializer, CreateUpdateFederalStateSerializer




class CreateFederalStateListView(ListCreateAPIView):
    permission_classes = [IsAdminUser]

    queryset = FederalState.objects.all()

    def get_serializer_class(self):
        if self.request.method == 'GET':
            return ListFederalStateSerializer
        return CreateUpdateFederalStateSerializer




class UpdateFederalStateListView(RetrieveUpdateDestroyAPIView):
    permission_classes = [IsAdminUser]
    queryset = FederalState.objects.all()

    def get_serializer_class(self):
        if self.request.method == 'GET':
            return ListFederalStateSerializer
        return CreateUpdateFederalStateSerializer