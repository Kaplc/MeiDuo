from rest_framework import serializers

from goods.models import SpecificationOption, SPUSpecification


class SpecificationOptionSerializer(serializers.ModelSerializer):
    """
        规格选项
    """
    spec_id = serializers.IntegerField()
    spec = serializers.StringRelatedField()

    class Meta:
        model = SpecificationOption
        fields = ('id', 'value', 'spec_id', 'spec')


class SPUSpecificationSerializer(serializers.ModelSerializer):
    """
        规格名称
    """
    class Meta:
        model = SPUSpecification

