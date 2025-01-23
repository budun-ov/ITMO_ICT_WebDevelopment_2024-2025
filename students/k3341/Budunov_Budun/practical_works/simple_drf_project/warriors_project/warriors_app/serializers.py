from rest_framework import serializers
from .models import Warrior, Profession, Skill, SkillOfWarrior


class WarriorSerializer(serializers.ModelSerializer):

  class Meta:
     model = Warrior
     fields = "__all__"

class SkillSerializer(serializers.ModelSerializer):

  class Meta:
     model = Skill
     fields = "__all__"

class ProfessionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Profession
        fields = "__all__"

class SkillOfWarriorSerializer(serializers.ModelSerializer):
    skill = SkillSerializer()

    class Meta:
        model = SkillOfWarrior
        fields = ['skill', 'level']

class WarriorProfessionSerializer(serializers.ModelSerializer):
    profession = ProfessionSerializer()

    class Meta:
        model = Warrior
        fields = ['id', 'name', 'race', 'level', 'profession']

class WarriorSkillsSerializer(serializers.ModelSerializer):
    skills = SkillOfWarriorSerializer(source='skillofwarrior_set', many=True)

    class Meta:
        model = Warrior
        fields = ['id', 'name', 'race', 'level', 'skills']

class WarriorDetailSerializer(serializers.ModelSerializer):
    profession = ProfessionSerializer()
    skills = SkillOfWarriorSerializer(source='skillofwarrior_set', many=True)

    class Meta:
        model = Warrior
        fields = ['id', 'name', 'race', 'level', 'profession', 'skills']

    def update(self, instance, validated_data):
        # Обновляем простые поля
        instance.name = validated_data.get('name', instance.name)
        instance.race = validated_data.get('race', instance.race)
        instance.level = validated_data.get('level', instance.level)

        # Обновляем профессию
        profession_data = validated_data.pop('profession', None)
        if profession_data:
            profession, _ = Profession.objects.get_or_create(**profession_data)
            instance.profession = profession

        # Обновляем навыки
        skills_data = validated_data.pop('skillofwarrior_set', [])
        if skills_data:
            # Удаляем старые записи навыков
            instance.skillofwarrior_set.all().delete()
            # Создаем новые записи навыков
            for skill_data in skills_data:
                skill_info = skill_data.pop('skill')
                skill, _ = Skill.objects.get_or_create(**skill_info)
                SkillOfWarrior.objects.create(
                    warrior=instance,
                    skill=skill,
                    level=skill_data.get('level', 0)
                )

        instance.save()
        return instance

class SkillCreateSerializer(serializers.Serializer):
    title = serializers.CharField(max_length=120)
    description = serializers.CharField()

    def create(self, validated_data):
       skill = Skill(**validated_data)
       skill.save()
       return skill

class ProfessionCreateSerializer(serializers.Serializer):
    title = serializers.CharField(max_length=120)
    description = serializers.CharField()

    def create(self, validated_data):
       profession = Profession(**validated_data)
       profession.save()
       return profession
