-- Foreign key constraints (executed last)
SET search_path = platform_center, public;
ALTER TABLE "platform_center"."user_push_category_weight" ADD CONSTRAINT "user_push_category_weight_push_config_id_fkey" FOREIGN KEY ("push_config_id") REFERENCES "platform_center"."user_push_config" ("id") ON DELETE CASCADE ON UPDATE RESTRICT;
ALTER TABLE "platform_center"."user_push_notify_channel" ADD CONSTRAINT "user_push_notify_channel_push_config_id_fkey" FOREIGN KEY ("push_config_id") REFERENCES "platform_center"."user_push_config" ("id") ON DELETE CASCADE ON UPDATE RESTRICT;

