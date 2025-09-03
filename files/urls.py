from django.urls import path
from . import views


urlpatterns = [
    path('', views.dashboard, name='dashboard'),
    path('tenant/<int:tenant_id>/', views.tenant_detail, name='tenant_detail'),
    path('add-tenant/', views.add_tenant, name='add_tenant'),

    # Uploads
    path('upload/', views.upload_document, name='upload_document'),
    path('upload-multiple/', views.upload_documents_by_type, name='upload_documents_by_type'),
    path('upload-docs/', views.upload_documents_by_type, name='upload_documents_by_type'),

    # Document and tenant actions
    path('expired/', views.expired_documents, name='expired_documents'),
    path('tenant/<int:tenant_id>/delete/', views.delete_tenant, name='delete_tenant'),
    path('document/<int:doc_id>/delete/', views.delete_document, name='delete_document'),
    path('document/<int:doc_id>/update-expiry/', views.update_expiry_date, name='update_expiry_date'),
    path('upload/by-type/<int:tenant_id>/', views.upload_documents_by_type, name='upload_documents_by_type'),
    path('tenant-status/', views.tenant_document_status, name='tenant_status'),
    path('tenant/<int:tenant_id>/send-reminder/', views.send_email_reminder, name='send_email_reminder'),
    path('tenant/<int:tenant_id>/update-email/', views.update_tenant_email, name='update_tenant_email'),
    path('export/expired-documents/', views.export_expired_documents_excel, name='export_expired_documents'),
    path('send-reminders/', views.send_reminders_to_all_tenants, name='send_reminders_to_all_tenants'),
    path('email-reminder-logs/', views.email_reminder_logs_view, name='email_reminder_logs'),
    path('email-reminder-logs/delete-all/', views.delete_all_email_logs, name='delete_all_email_logs'),
    path('export/email-logs/', views.export_email_logs_excel, name='export_email_logs_excel'),
    path('bulk-upload-tenants/', views.bulk_upload_tenants, name='bulk_upload_tenants'),
    path('download-tenant-template/', views.download_tenant_template, name='download_tenant_template'),
    path('tenant/<int:tenant_id>/share-documents/', views.share_documents, name='share_documents'),
    path('download/<int:document_id>/', views.download_document, name='download_document'),
    path("track-expiry/", views.track_expiry, name="track_expiry"),
    path("expiry-data/", views.expiry_data, name="expiry_data"), 
    path('export-tracked-expiry/', views.export_tracked_expiry_excel, name='export_tracked_expiry_excel'),
    path('calculate-expiry/', views.calculate_expiry, name='calculate_expiry'),
    path('update-commencement-date/', views.update_commencement_date, name='update_commencement_date'),
    path('unit/delete/<int:unit_id>/', views.delete_unit, name='delete_unit'),
    path('unit/update/<int:unit_id>/', views.update_unit, name='update_unit'),
    path('unit/add/<int:tenant_id>/', views.add_unit, name='add_unit'),
    path('export-tenants/', views.export_tenants_excel, name='export_tenants_excel'),
    path('documents/<int:doc_id>/archive/', views.archive_documents, name='archive_document'),
    path("archives/", views.archived_documents_list, name="archived_documents_list"),
    path('archives/restore/<int:archived_id>/', views.restore_archived_document, name='restore_archived_document'),
    path('archives/download/<int:archived_id>/', views.download_archived_document, name='download_archived_document'),
    path('archives/delete/<int:archived_id>/', views.delete_archived_document, name='delete_archived_document'),
    path("tenant/<int:tenant_id>/update_date/", views.update_tenant_date, name="update_tenant_date"),
    path("tenant/<int:tenant_id>/update_rate/", views.update_tenant_rate, name="update_tenant_rate"),
    # urls.py
    path('data-point/', views.data_point_view, name='data_point'),
    path('tenant/<int:tenant_id>/update_date_rate/', views.update_tenant_date_rate, name='update_tenant_date_rate'),





    



  





    # Analytics and management
    path('analytics/', views.analytics, name='analytics'),
    path('tenants-documents/', views.tenants_with_documents, name='tenants_documents'),

    # Authentication
    path('login/', views.login_view, name='login'),
    path('logout/', views.logout_view, name='logout'),
    path('profile/', views.profile_view, name='profile'),
]
