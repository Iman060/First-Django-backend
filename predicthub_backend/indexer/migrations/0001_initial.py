# Generated migration for OnchainTransaction and OnchainEventLog models

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ("contenttypes", "0002_remove_content_type_name"),
        ("markets", "0002_initial"),
    ]

    operations = [
        migrations.CreateModel(
            name='OnchainTransaction',
            fields=[
                ('id', models.BigAutoField(primary_key=True, serialize=False)),
                ('tx_hash', models.CharField(max_length=80, unique=True)),
                ('network', models.CharField(max_length=32)),
                ('block_number', models.BigIntegerField(null=True)),
                ('status', models.CharField(choices=[('PENDING', 'Pending'), ('SUCCESS', 'Success'), ('FAILED', 'Failed')], max_length=16)),
                ('error_message', models.TextField(blank=True)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
            ],
            options={
                'ordering': ['-created_at'],
            },
        ),
        migrations.CreateModel(
            name='OnchainEventLog',
            fields=[
                ('id', models.BigAutoField(primary_key=True, serialize=False)),
                ('event_name', models.CharField(max_length=64)),
                ('tx_hash', models.CharField(max_length=80)),
                ('log_index', models.IntegerField()),
                ('user_address', models.CharField(blank=True, max_length=64)),
                ('payload_json', models.JSONField()),
                ('processed_at', models.DateTimeField(blank=True, null=True)),
                ('duplicate', models.BooleanField(default=False)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('market', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='onchain_event_logs', to='markets.market')),
            ],
            options={
                'ordering': ['-created_at'],
                'unique_together': {('tx_hash', 'log_index')},
            },
        ),
        migrations.AddIndex(
            model_name='onchaintransaction',
            index=models.Index(fields=['tx_hash'], name='indexer_onc_tx_hash_idx'),
        ),
        migrations.AddIndex(
            model_name='onchaintransaction',
            index=models.Index(fields=['network', 'status'], name='indexer_onc_network_status_idx'),
        ),
        migrations.AddIndex(
            model_name='onchaintransaction',
            index=models.Index(fields=['block_number'], name='indexer_onc_block_number_idx'),
        ),
        migrations.AddIndex(
            model_name='onchaineventlog',
            index=models.Index(fields=['tx_hash'], name='indexer_onc_tx_hash_2_idx'),
        ),
        migrations.AddIndex(
            model_name='onchaineventlog',
            index=models.Index(fields=['market'], name='indexer_onc_market_idx'),
        ),
        migrations.AddIndex(
            model_name='onchaineventlog',
            index=models.Index(fields=['event_name'], name='indexer_onc_event_name_idx'),
        ),
        migrations.AddIndex(
            model_name='onchaineventlog',
            index=models.Index(fields=['user_address'], name='indexer_onc_user_address_idx'),
        ),
    ]

