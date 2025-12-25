from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0007_user_groups_user_last_login_user_user_permissions'),
    ]

    operations = [
        migrations.RunSQL(
            # Drop existing FK that references auth_user (if present) and recreate referencing users_user
            sql=(
                "ALTER TABLE django_admin_log DROP CONSTRAINT IF EXISTS django_admin_log_user_id_c564eba6_fk_auth_user_id;"
                "ALTER TABLE django_admin_log ADD CONSTRAINT django_admin_log_user_id_fk_users_user_user_id "
                "FOREIGN KEY (user_id) REFERENCES users_user(user_id) DEFERRABLE INITIALLY DEFERRED;"
            ),
            reverse_sql=(
                "ALTER TABLE django_admin_log DROP CONSTRAINT IF EXISTS django_admin_log_user_id_fk_users_user_user_id;"
                "ALTER TABLE django_admin_log ADD CONSTRAINT django_admin_log_user_id_c564eba6_fk_auth_user_id "
                "FOREIGN KEY (user_id) REFERENCES auth_user(id) DEFERRABLE INITIALLY DEFERRED;"
            ),
        )
    ]
