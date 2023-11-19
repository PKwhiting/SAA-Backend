# Generated by Django 4.2.6 on 2023-11-19 07:49

from django.conf import settings
import django.contrib.auth.models
import django.contrib.auth.validators
from django.db import migrations, models
import django.db.models.deletion
import django.utils.timezone


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('auth', '0014_remove_user_phone_number'),
    ]

    operations = [
        migrations.CreateModel(
            name='User',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('password', models.CharField(max_length=128, verbose_name='password')),
                ('last_login', models.DateTimeField(blank=True, null=True, verbose_name='last login')),
                ('is_superuser', models.BooleanField(default=False, help_text='Designates that this user has all permissions without explicitly assigning them.', verbose_name='superuser status')),
                ('username', models.CharField(error_messages={'unique': 'A user with that username already exists.'}, help_text='Required. 150 characters or fewer. Letters, digits and @/./+/-/_ only.', max_length=150, unique=True, validators=[django.contrib.auth.validators.UnicodeUsernameValidator()], verbose_name='username')),
                ('first_name', models.CharField(blank=True, max_length=150, verbose_name='first name')),
                ('last_name', models.CharField(blank=True, max_length=150, verbose_name='last name')),
                ('email', models.EmailField(blank=True, max_length=254, verbose_name='email address')),
                ('is_staff', models.BooleanField(default=False, help_text='Designates whether the user can log into this admin site.', verbose_name='staff status')),
                ('is_active', models.BooleanField(default=True, help_text='Designates whether this user should be treated as active. Unselect this instead of deleting accounts.', verbose_name='active')),
                ('date_joined', models.DateTimeField(default=django.utils.timezone.now, verbose_name='date joined')),
                ('phone_number', models.CharField(blank=True, max_length=15, null=True)),
                ('profile_picture', models.ImageField(blank=True, null=True, upload_to='profile_pictures/')),
                ('is_seller', models.BooleanField(blank=True, default=False, null=True)),
                ('is_buyer', models.BooleanField(blank=True, default=False, null=True)),
                ('is_admin', models.BooleanField(blank=True, default=False, null=True)),
                ('groups', models.ManyToManyField(blank=True, help_text='The groups this user belongs to. A user will get all permissions granted to each of their groups.', related_name='user_set', related_query_name='user', to='auth.group', verbose_name='groups')),
                ('user_permissions', models.ManyToManyField(blank=True, help_text='Specific permissions for this user.', related_name='user_set', related_query_name='user', to='auth.permission', verbose_name='user permissions')),
            ],
            options={
                'verbose_name': 'user',
                'verbose_name_plural': 'users',
                'abstract': False,
            },
            managers=[
                ('objects', django.contrib.auth.models.UserManager()),
            ],
        ),
        migrations.CreateModel(
            name='Car',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('auction', models.CharField(choices=[('SAA', 'SAA'), ('COPART', 'COPART'), ('IAA', 'IAA')], default='SAA', max_length=100)),
                ('vehicle_auction_link', models.CharField(blank=True, max_length=100, null=True)),
                ('year', models.IntegerField()),
                ('make', models.CharField(max_length=100)),
                ('model', models.CharField(max_length=100)),
                ('VIN', models.CharField(max_length=100)),
                ('title_code', models.CharField(blank=True, max_length=100)),
                ('color', models.CharField(max_length=100)),
                ('engine', models.CharField(blank=True, max_length=100)),
                ('engine_displacement', models.CharField(blank=True, default=0.0, max_length=100)),
                ('cylinders', models.IntegerField(blank=True)),
                ('transmission', models.CharField(blank=True, max_length=100)),
                ('drive_type', models.CharField(blank=True, max_length=100)),
                ('vehicle_type', models.CharField(blank=True, max_length=100)),
                ('fuel_type', models.CharField(blank=True, max_length=100)),
                ('keys', models.IntegerField(blank=True, null=True)),
                ('mileage', models.IntegerField()),
                ('starting_bid', models.DecimalField(decimal_places=2, max_digits=10)),
                ('current_bid', models.DecimalField(blank=True, decimal_places=2, default=0.0, max_digits=10)),
                ('reserve_price', models.DecimalField(blank=True, decimal_places=2, max_digits=10)),
                ('description', models.TextField(blank=True, max_length=1000, null=True)),
                ('active', models.BooleanField(default=True)),
                ('condition', models.CharField(blank=True, max_length=100)),
                ('vehicle_location', models.TextField()),
                ('sale_date', models.DateTimeField()),
                ('last_updated', models.DateTimeField(auto_now=True)),
                ('image_1', models.ImageField(blank=True, upload_to='cars')),
                ('image_2', models.ImageField(blank=True, upload_to='cars')),
                ('image_3', models.ImageField(blank=True, upload_to='cars')),
                ('image_4', models.ImageField(blank=True, upload_to='cars')),
                ('image_5', models.ImageField(blank=True, upload_to='cars')),
                ('image_6', models.ImageField(blank=True, upload_to='cars')),
                ('image_7', models.ImageField(blank=True, upload_to='cars')),
                ('image_8', models.ImageField(blank=True, upload_to='cars')),
                ('image_9', models.ImageField(blank=True, upload_to='cars')),
                ('image_10', models.ImageField(blank=True, upload_to='cars')),
                ('image_1_url', models.URLField(blank=True, null=True)),
                ('image_2_url', models.URLField(blank=True, null=True)),
                ('image_3_url', models.URLField(blank=True, null=True)),
                ('image_4_url', models.URLField(blank=True, null=True)),
                ('image_5_url', models.URLField(blank=True, null=True)),
                ('image_6_url', models.URLField(blank=True, null=True)),
                ('image_7_url', models.URLField(blank=True, null=True)),
                ('image_8_url', models.URLField(blank=True, null=True)),
                ('image_9_url', models.URLField(blank=True, null=True)),
                ('image_10_url', models.URLField(blank=True, null=True)),
                ('vehicle_starts', models.BooleanField(default=False)),
                ('vehicle_drives', models.BooleanField(default=False)),
                ('bumper_damage', models.BooleanField(default=False)),
                ('driver_headlight_damage', models.BooleanField(default=False)),
                ('passenger_headlight_damage', models.BooleanField(default=False)),
                ('hood_damage', models.BooleanField(default=False)),
                ('roof_damage', models.BooleanField(default=False)),
                ('driver_fender_damage', models.BooleanField(default=False)),
                ('passenger_fender_damage', models.BooleanField(default=False)),
                ('driver_door_damage', models.BooleanField(default=False)),
                ('passenger_door_damage', models.BooleanField(default=False)),
                ('driver_rear_door_damage', models.BooleanField(default=False)),
                ('passenger_rear_door_damage', models.BooleanField(default=False)),
                ('driver_rocker_damage', models.BooleanField(default=False)),
                ('passenger_rocker_damage', models.BooleanField(default=False)),
                ('driver_rear_wheel_arch_damage', models.BooleanField(default=False)),
                ('passenger_rear_wheel_arch_damage', models.BooleanField(default=False)),
                ('driver_rear_quarter_damage', models.BooleanField(default=False)),
                ('passenger_rear_quarter_damage', models.BooleanField(default=False)),
                ('trunk_damage', models.BooleanField(default=False)),
                ('rear_bumper_damage', models.BooleanField(default=False)),
                ('driver_tail_light_damage', models.BooleanField(default=False)),
                ('passenger_tail_light_damage', models.BooleanField(default=False)),
                ('driver_mirror_damage', models.BooleanField(default=False)),
                ('passenger_mirror_damage', models.BooleanField(default=False)),
                ('windshield_damage', models.BooleanField(default=False)),
                ('driver_window_damage', models.BooleanField(default=False)),
                ('passenger_window_damage', models.BooleanField(default=False)),
                ('driver_rear_window_damage', models.BooleanField(default=False)),
                ('passenger_rear_window_damage', models.BooleanField(default=False)),
                ('back_glass_damage', models.BooleanField(default=False)),
                ('truck_bed_damage', models.BooleanField(default=False)),
                ('creator', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='VehicleFilter',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('make', models.CharField(blank=True, max_length=50, null=True)),
                ('model', models.CharField(blank=True, max_length=50, null=True)),
                ('start_year', models.IntegerField(blank=True, null=True)),
                ('end_year', models.IntegerField(blank=True, null=True)),
                ('filter_name', models.CharField(max_length=50)),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='SavedVehicle',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('saved_vehicle', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='simplicarbackend.car')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='Bid',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('bid_amount', models.DecimalField(decimal_places=2, max_digits=10)),
                ('bid_date', models.DateTimeField(auto_now=True)),
                ('bid_vehicle', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='simplicarbackend.car')),
                ('bidder', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]
