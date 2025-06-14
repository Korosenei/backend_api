# Generated by Django 5.1.7 on 2025-05-26 18:08

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('_enseignements', '0001_initial'),
        ('_users', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='departement',
            name='chef',
            field=models.OneToOneField(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='departement_dirige', to='_users.chefdepartement', verbose_name='Chef de département'),
        ),
        migrations.AddField(
            model_name='departement',
            name='etablissement',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='departements', to='_enseignements.etablissement', verbose_name='Établissement de rattachement'),
        ),
        migrations.AddField(
            model_name='filiere',
            name='departement',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='filieres', to='_enseignements.departement', verbose_name='Département responsable'),
        ),
        migrations.AddField(
            model_name='filiere',
            name='responsable',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='filieres_responsables', to='_users.enseignant', verbose_name='Responsable pédagogique'),
        ),
        migrations.AddField(
            model_name='classe',
            name='filiere',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='classes', to='_enseignements.filiere', verbose_name='Filière'),
        ),
        migrations.AddField(
            model_name='etablissement',
            name='localite',
            field=models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, related_name='etablissements', to='_enseignements.localite', verbose_name='Localisation'),
        ),
        migrations.AddField(
            model_name='matiere',
            name='enseignant',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='matieres', to='_users.enseignant', verbose_name='Enseignant responsable'),
        ),
        migrations.AddField(
            model_name='classe',
            name='matieres',
            field=models.ManyToManyField(blank=True, related_name='classes', to='_enseignements.matiere', verbose_name='Matières enseignées'),
        ),
        migrations.AddField(
            model_name='module',
            name='responsable',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='modules_responsables', to='_users.enseignant', verbose_name='Responsable du module'),
        ),
        migrations.AddField(
            model_name='matiere',
            name='module',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='matieres', to='_enseignements.module', verbose_name='Module parent'),
        ),
        migrations.AddField(
            model_name='module',
            name='niveau',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='_enseignements.niveau', verbose_name='Niveau concerné'),
        ),
        migrations.AddField(
            model_name='classe',
            name='niveau',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='classes', to='_enseignements.niveau', verbose_name='Niveau académique'),
        ),
        migrations.AddField(
            model_name='ressourcepdf',
            name='auteur',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='_users.enseignant', verbose_name='Auteur'),
        ),
        migrations.AddField(
            model_name='ressourcepdf',
            name='matiere',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='ressources_pdf', to='_enseignements.matiere', verbose_name='Matière associée'),
        ),
        migrations.AddField(
            model_name='ressourcevideo',
            name='auteur',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='_users.enseignant', verbose_name='Auteur'),
        ),
        migrations.AddField(
            model_name='ressourcevideo',
            name='matiere',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='ressources_video', to='_enseignements.matiere', verbose_name='Matière associée'),
        ),
        migrations.AddField(
            model_name='module',
            name='semestre',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='_enseignements.semestre', verbose_name='Semestre concerné'),
        ),
        migrations.AddField(
            model_name='specialite',
            name='filiere',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='specialites', to='_enseignements.filiere', verbose_name='Filière parente'),
        ),
        migrations.AddField(
            model_name='module',
            name='specialite',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='_enseignements.specialite', verbose_name='Spécialité concernée'),
        ),
        migrations.AddField(
            model_name='etablissement',
            name='statut_etablissement',
            field=models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, related_name='etablissements', to='_enseignements.statutetablissement', verbose_name='Statut juridique'),
        ),
        migrations.AddField(
            model_name='etablissement',
            name='type_etablissement',
            field=models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, related_name='etablissements', to='_enseignements.typeetablissement', verbose_name="Type d'établissement"),
        ),
        migrations.AddConstraint(
            model_name='departement',
            constraint=models.UniqueConstraint(fields=('nom', 'etablissement'), name='unique_departement_etablissement'),
        ),
        migrations.AddConstraint(
            model_name='departement',
            constraint=models.UniqueConstraint(fields=('sigle', 'etablissement'), name='unique_sigle_departement'),
        ),
        migrations.AddConstraint(
            model_name='filiere',
            constraint=models.UniqueConstraint(fields=('nom', 'departement'), name='unique_filiere_departement'),
        ),
        migrations.AddConstraint(
            model_name='matiere',
            constraint=models.UniqueConstraint(fields=('code', 'module'), name='unique_matiere_module'),
        ),
        migrations.AddConstraint(
            model_name='classe',
            constraint=models.UniqueConstraint(fields=('nom', 'filiere', 'annee_scolaire'), name='unique_classe_annee'),
        ),
        migrations.AddConstraint(
            model_name='specialite',
            constraint=models.UniqueConstraint(fields=('nom', 'filiere'), name='unique_specialite_filiere'),
        ),
        migrations.AddConstraint(
            model_name='module',
            constraint=models.UniqueConstraint(fields=('code', 'specialite'), name='unique_module_specialite'),
        ),
        migrations.AddConstraint(
            model_name='etablissement',
            constraint=models.UniqueConstraint(fields=('nom', 'localite'), name='unique_etablissement_localite'),
        ),
    ]
