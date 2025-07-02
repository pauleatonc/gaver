from rest_framework import serializers
from django.contrib.auth import authenticate
from django.contrib.auth.models import User


class UserSerializer(serializers.ModelSerializer):
    """Serializer para el modelo User de Django"""
    class Meta:
        model = User
        fields = ('id', 'username', 'email', 'first_name', 'last_name')
        read_only_fields = ('id',)


class LoginSerializer(serializers.Serializer):
    """Serializer para el login de usuarios"""
    email = serializers.EmailField()
    password = serializers.CharField(write_only=True)

    def validate(self, attrs):
        email = attrs.get('email')
        password = attrs.get('password')

        if email and password:
            # Buscar el usuario por email
            try:
                user = User.objects.get(email=email)
                # Autenticar con username (que es requerido por Django)
                user = authenticate(username=user.username, password=password)
                if user:
                    attrs['user'] = user
                    return attrs
                else:
                    raise serializers.ValidationError('Credenciales inválidas.')
            except User.DoesNotExist:
                raise serializers.ValidationError('No existe un usuario con este email.')
        else:
            raise serializers.ValidationError('Debe proporcionar email y contraseña.')

        return attrs


class RegisterSerializer(serializers.ModelSerializer):
    """Serializer para el registro de usuarios"""
    password = serializers.CharField(write_only=True, min_length=6)
    confirm_password = serializers.CharField(write_only=True)
    username = serializers.CharField(required=False, allow_blank=True, allow_null=True)

    class Meta:
        model = User
        fields = ('username', 'email', 'first_name', 'last_name', 'password', 'confirm_password')

    def validate(self, attrs):
        if attrs['password'] != attrs['confirm_password']:
            raise serializers.ValidationError("Las contraseñas no coinciden.")
        
        # Validar que el email sea único
        email = attrs.get('email')
        if email and User.objects.filter(email=email).exists():
            raise serializers.ValidationError({
                'email': ['Este email ya está registrado.']
            })
        
        return attrs

    def create(self, validated_data):
        validated_data.pop('confirm_password')
        
        # Generar username automáticamente si no se proporciona
        if not validated_data.get('username') or validated_data.get('username').strip() == '':
            first_name = validated_data.get('first_name', '').lower().replace(' ', '')
            last_name = validated_data.get('last_name', '').lower().replace(' ', '')
            
            if first_name and last_name:
                base_username = f"{first_name}_{last_name}"
            elif first_name:
                base_username = first_name
            elif last_name:
                base_username = last_name
            else:
                base_username = f"user_{User.objects.count() + 1}"
            
            # Si el username ya existe, agregar un número
            username = base_username
            counter = 1
            while User.objects.filter(username=username).exists():
                username = f"{base_username}_{counter}"
                counter += 1
            
            validated_data['username'] = username
        
        user = User.objects.create_user(**validated_data)
        return user 