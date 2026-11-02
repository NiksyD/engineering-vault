## Table `schema_migrations`

### Columns

| Name | Type | Constraints |
|------|------|-------------|
| `version` | `varchar` | Primary |
| `applied_at` | `timestamptz` |  Nullable |

## Table `modules`

### Columns

| Name | Type | Constraints |
|------|------|-------------|
| `mod_id` | `text` | Primary |
| `mentor_id` | `uuid` |  |
| `mod_title` | `text` |  |
| `mod_description` | `text` |  |
| `mod_stack` | `_text` |  |
| `mod_created_at` | `timestamptz` |  |
| `mod_updated_at` | `timestamptz` |  |
| `mod_rating` | `numeric` |  Nullable |
| `mod_status` | `text` |  Nullable |
| `mod_is_pinned` | `bool` |  Nullable |
| `mod_price` | `numeric` |  |
| `mod_feedback_type` | `text` |  |
| `edit_unlocked_at` | `timestamptz` |  Nullable |
| `edit_unlocked_reason` | `text` |  Nullable |
| `edit_unlocked_by` | `uuid` |  Nullable |

## Table `topics`

### Columns

| Name | Type | Constraints |
|------|------|-------------|
| `topic_id` | `uuid` | Primary |
| `track_id` | `text` |  |
| `topic_title` | `text` |  |
| `topic_description` | `text` |  |
| `topic_order_index` | `int4` |  |

## Table `test_cases`

### Columns

| Name | Type | Constraints |
|------|------|-------------|
| `test_id` | `uuid` | Primary |
| `item_id` | `uuid` |  |
| `test_input` | `text` |  |
| `test_expected_output` | `text` |  |
| `test_is_sample` | `bool` |  |
| `test_order_index` | `int4` |  |

## Table `submissions`

### Columns

| Name | Type | Constraints |
|------|------|-------------|
| `sub_id` | `uuid` | Primary |
| `user_id` | `uuid` |  |
| `item_id` | `text` |  |
| `sub_language` | `text` |  Nullable |
| `sub_code` | `text` |  Nullable |
| `sub_status` | `text` |  |
| `sub_verdict` | `jsonb` |  Nullable |
| `sub_submitted_at` | `timestamptz` |  |

## Table `mentor_profiles`

### Columns

| Name | Type | Constraints |
|------|------|-------------|
| `ment_id` | `uuid` | Primary |
| `user_id` | `uuid` |  Unique |
| `ment_title` | `text` |  |
| `ment_biography` | `text` |  |
| `ment_rating` | `numeric` |  |
| `ment_github_url` | `text` |  |
| `ment_linkedin` | `text` |  |
| `ment_website_url` | `text` |  |
| `ment_created_at` | `timestamptz` |  |
| `ment_updated_at` | `timestamptz` |  |
| `ment_approval_status` | `text` |  Nullable |
| `ment_id_document_url` | `text` |  |
| `ment_credentials` | `_text` |  |

## Table `notifications`

### Columns

| Name | Type | Constraints |
|------|------|-------------|
| `notif_id` | `uuid` | Primary |
| `user_id` | `uuid` |  |
| `notif_title` | `text` |  |
| `notif_message` | `text` |  |
| `notif_is_read` | `bool` |  |
| `notif_type` | `text` |  |
| `notif_created_at` | `timestamptz` |  |
| `notif_source_id` | `uuid` |  Nullable |

## Table `profiles`

### Columns

| Name | Type | Constraints |
|------|------|-------------|
| `user_id` | `uuid` | Primary |
| `user_first_name` | `text` |  |
| `user_last_name` | `text` |  |
| `user_email` | `text` |  Unique |
| `user_created_at` | `timestamptz` |  |
| `user_updated_at` | `timestamptz` |  |
| `user_role` | `text` |  |
| `user_email_notifications` | `bool` |  |
| `user_avatar_url` | `text` |  |
| `user_is_active` | `bool` |  |
| `user_onboarded` | `bool` |  |

## Table `ai_audits`

### Columns

| Name | Type | Constraints |
|------|------|-------------|
| `audit_id` | `uuid` | Primary |
| `sub_id` | `uuid` |  |
| `audit_findings` | `jsonb` |  |
| `audit_is_flagged` | `bool` |  |
| `audit_audited_at` | `timestamptz` |  |

## Table `user_practice_saves`

### Columns

| Name | Type | Constraints |
|------|------|-------------|
| `user_id` | `uuid` | Primary |
| `track_id` | `text` | Primary |
| `ups_saved_at` | `timestamptz` |  Nullable |

## Table `user_practice_progress`

### Columns

| Name | Type | Constraints |
|------|------|-------------|
| `user_id` | `uuid` | Primary |
| `track_id` | `text` | Primary |
| `upp_completion` | `int4` |  Nullable |
| `upp_updated_at` | `timestamptz` |  Nullable |

## Table `go_schema_migrations`

### Columns

| Name | Type | Constraints |
|------|------|-------------|
| `version` | `int8` | Primary |
| `dirty` | `bool` |  |

## Table `activities`

### Columns

| Name | Type | Constraints |
|------|------|-------------|
| `act_id` | `uuid` | Primary |
| `topic_id` | `uuid` |  Nullable |
| `act_title` | `text` |  |
| `act_description` | `text` |  |
| `act_category` | `text` |  |
| `act_order_index` | `int4` |  |
| `act_created_at` | `timestamptz` |  |
| `act_difficulty` | `varchar` |  Nullable |
| `act_status` | `text` |  |
| `track_id` | `text` |  Nullable |
| `is_locked` | `bool` |  |
| `edit_unlocked_at` | `timestamptz` |  Nullable |
| `edit_unlocked_reason` | `text` |  Nullable |
| `edit_unlocked_by` | `uuid` |  Nullable |

## Table `code_details`

### Columns

| Name | Type | Constraints |
|------|------|-------------|
| `item_id` | `uuid` | Primary |
| `target_time` | `text` |  |
| `target_space` | `text` |  |
| `code_task_style` | `text` |  |
| `starter_codes` | `jsonb` |  |
| `solutions` | `jsonb` |  |
| `languages` | `jsonb` |  Nullable |

## Table `module_reviews`

### Columns

| Name | Type | Constraints |
|------|------|-------------|
| `review_id` | `uuid` | Primary |
| `track_id` | `text` |  |
| `user_id` | `uuid` |  |
| `rating` | `int4` |  |
| `comment` | `text` |  |
| `review_created_at` | `timestamptz` |  |
| `review_updated_at` | `timestamptz` |  |

## Table `user_streaks`

### Columns

| Name | Type | Constraints |
|------|------|-------------|
| `user_id` | `uuid` | Primary |
| `current_streak` | `int4` |  |
| `longest_streak` | `int4` |  |
| `last_activity_date` | `date` |  Nullable |
| `updated_at` | `timestamptz` |  Nullable |

## Table `module_reports`

### Columns

| Name | Type | Constraints |
|------|------|-------------|
| `report_id` | `uuid` | Primary |
| `mod_id` | `text` |  |
| `user_id` | `uuid` |  Nullable |
| `report_reason` | `text` |  |
| `report_details` | `text` |  |
| `report_status` | `text` |  |
| `admin_notes` | `text` |  Nullable |
| `resolved_by` | `uuid` |  Nullable |
| `report_created_at` | `timestamptz` |  |
| `report_resolved_at` | `timestamptz` |  Nullable |
| `act_id` | `uuid` |  Nullable |
| `report_source` | `text` |  |

## Table `assessments`

### Columns

| Name | Type | Constraints |
|------|------|-------------|
| `id` | `uuid` | Primary |
| `title` | `text` |  |
| `description` | `text` |  Nullable |
| `stack` | `_text` |  Nullable |
| `difficulty` | `text` |  Nullable |
| `duration_mins` | `int4` |  |
| `passing_score` | `int4` |  |
| `max_attempts` | `int4` |  |
| `status` | `text` |  |
| `mentor_id` | `uuid` |  Nullable |
| `created_at` | `timestamptz` |  |
| `updated_at` | `timestamptz` |  |
| `price` | `numeric` |  |
| `price_coins` | `int4` |  |
| `edit_unlocked_at` | `timestamptz` |  Nullable |
| `edit_unlocked_reason` | `text` |  Nullable |
| `edit_unlocked_by` | `uuid` |  Nullable |

## Table `assessment_challenges`

### Columns

| Name | Type | Constraints |
|------|------|-------------|
| `id` | `uuid` | Primary |
| `assessment_id` | `uuid` |  |
| `source_activity_id` | `uuid` |  Nullable |
| `title` | `text` |  |
| `problem_statement` | `text` |  |
| `starter_code` | `text` |  |
| `language` | `text` |  |
| `difficulty` | `text` |  Nullable |
| `order_index` | `int4` |  |
| `test_cases` | `jsonb` |  Nullable |
| `created_at` | `timestamptz` |  |
| `solution_code` | `text` |  Nullable |
| `solutions` | `jsonb` |  Nullable |
| `is_locked` | `bool` |  |
| `edit_unlocked_at` | `timestamptz` |  Nullable |
| `edit_unlocked_reason` | `text` |  Nullable |
| `edit_unlocked_by` | `uuid` |  Nullable |

## Table `assessment_reports`

### Columns

| Name | Type | Constraints |
|------|------|-------------|
| `report_id` | `uuid` | Primary |
| `assessment_id` | `uuid` |  |
| `user_id` | `uuid` |  Nullable |
| `report_reason` | `text` |  |
| `report_details` | `text` |  |
| `report_status` | `text` |  |
| `admin_notes` | `text` |  Nullable |
| `resolved_by` | `uuid` |  Nullable |
| `report_created_at` | `timestamptz` |  |
| `report_resolved_at` | `timestamptz` |  Nullable |
| `challenge_id` | `uuid` |  Nullable |
| `report_source` | `text` |  |

## Table `user_assessment_library`

### Columns

| Name | Type | Constraints |
|------|------|-------------|
| `id` | `uuid` | Primary |
| `user_id` | `uuid` |  |
| `assessment_id` | `uuid` |  |
| `status` | `text` |  |
| `best_score` | `int4` |  Nullable |
| `saved_at` | `timestamptz` |  |

## Table `hubs`

### Columns

| Name | Type | Constraints |
|------|------|-------------|
| `id` | `uuid` | Primary |
| `mentor_id` | `uuid` |  |
| `name` | `text` |  |
| `section` | `text` |  |
| `join_code` | `varchar` |  Unique |
| `target_language` | `text` |  |
| `description` | `text` |  Nullable |
| `settings` | `jsonb` |  |
| `is_archived` | `bool` |  |
| `created_at` | `timestamptz` |  |
| `updated_at` | `timestamptz` |  |
| `primary_module_id` | `text` |  Nullable |

## Table `hub_members`

### Columns

| Name | Type | Constraints |
|------|------|-------------|
| `id` | `uuid` | Primary |
| `hub_id` | `uuid` |  |
| `learner_id` | `uuid` |  |
| `role` | `text` |  |
| `joined_via` | `text` |  |
| `enrolled_at` | `timestamptz` |  |
| `status` | `text` |  |
| `requested_at` | `timestamptz` |  Nullable |

## Table `hub_invitations`

### Columns

| Name | Type | Constraints |
|------|------|-------------|
| `id` | `uuid` | Primary |
| `hub_id` | `uuid` |  |
| `invited_email` | `text` |  |
| `invited_by` | `uuid` |  |
| `status` | `text` |  |
| `created_at` | `timestamptz` |  |
| `accepted_at` | `timestamptz` |  Nullable |

## Table `hub_modules`

### Columns

| Name | Type | Constraints |
|------|------|-------------|
| `id` | `uuid` | Primary |
| `hub_id` | `uuid` |  |
| `module_id` | `text` |  |
| `display_order` | `int4` |  |
| `created_at` | `timestamptz` |  |

## Table `submission_feedback`

Direct mentor feedback, qualitative reviews, and grade overrides on learner activity submissions within a room.

### Columns

| Name | Type | Constraints |
|------|------|-------------|
| `id` | `uuid` | Primary |
| `submission_id` | `uuid` |  |
| `hub_id` | `uuid` |  |
| `mentor_id` | `uuid` |  |
| `learner_id` | `uuid` |  |
| `feedback_text` | `text` |  |
| `grade_override` | `text` |  Nullable |
| `status` | `text` |  |
| `created_at` | `timestamptz` |  |
| `updated_at` | `timestamptz` |  |

## Table `user_wallets`

### Columns

| Name | Type | Constraints |
|------|------|-------------|
| `user_id` | `uuid` | Primary |
| `balance_coins` | `int8` |  |
| `total_earned_coins` | `int8` |  |
| `created_at` | `timestamptz` |  |
| `updated_at` | `timestamptz` |  |

## Table `coin_transactions`

### Columns

| Name | Type | Constraints |
|------|------|-------------|
| `id` | `uuid` | Primary |
| `user_id` | `uuid` |  |
| `amount_coins` | `int4` |  |
| `balance_after` | `int8` |  |
| `tx_type` | `text` |  |
| `reference_id` | `text` |  Nullable |
| `description` | `text` |  |
| `created_at` | `timestamptz` |  |

## Table `hub_assessments`

### Columns

| Name | Type | Constraints |
|------|------|-------------|
| `id` | `uuid` | Primary |
| `hub_id` | `uuid` |  |
| `assessment_id` | `uuid` |  |
| `display_order` | `int4` |  |
| `created_at` | `timestamptz` |  |

## RLS Policies

### `hub_assessments`

| Policy | Command | Roles | Action | USING | WITH CHECK |
|--------|---------|-------|--------|-------|------------|
| `Members view hub assessments` | SELECT | public | PERMISSIVE | `(is_hub_member(hub_id, auth.uid()) OR is_hub_mentor(hub_id, auth.uid()) OR is_admin(auth.uid()))` | — |
| `Mentors manage hub assessments` | ALL | public | PERMISSIVE | `(is_hub_mentor(hub_id, auth.uid()) OR is_admin(auth.uid()))` | `(is_hub_mentor(hub_id, auth.uid()) OR is_admin(auth.uid()))` |

### `topics`

| Policy | Command | Roles | Action | USING | WITH CHECK |
|--------|---------|-------|--------|-------|------------|
| `Authenticated users can delete topics` | DELETE | authenticated | PERMISSIVE | `true` | — |
| `Authenticated users can insert topics` | INSERT | authenticated | PERMISSIVE | — | `true` |
| `Authenticated users can update topics` | UPDATE | authenticated | PERMISSIVE | `true` | `true` |
| `Public can view topics` | SELECT | public | PERMISSIVE | `true` | — |

### `code_details`

| Policy | Command | Roles | Action | USING | WITH CHECK |
|--------|---------|-------|--------|-------|------------|
| `Authenticated users can delete code_details` | DELETE | authenticated | PERMISSIVE | `true` | — |
| `Authenticated users can insert code_details` | INSERT | authenticated | PERMISSIVE | — | `true` |
| `Authenticated users can update code_details` | UPDATE | authenticated | PERMISSIVE | `true` | `true` |
| `Public can view code_details` | SELECT | public | PERMISSIVE | `true` | — |

### `test_cases`

| Policy | Command | Roles | Action | USING | WITH CHECK |
|--------|---------|-------|--------|-------|------------|
| `Authenticated users can delete test_cases` | DELETE | authenticated | PERMISSIVE | `true` | — |
| `Authenticated users can insert test_cases` | INSERT | authenticated | PERMISSIVE | — | `true` |
| `Public can view test_cases` | SELECT | public | PERMISSIVE | `true` | — |

### `submissions`

| Policy | Command | Roles | Action | USING | WITH CHECK |
|--------|---------|-------|--------|-------|------------|
| `Mentors can view classroom student submissions` | SELECT | authenticated | PERMISSIVE | `(is_admin(auth.uid()) OR (EXISTS ( SELECT 1    FROM (hub_members rm      JOIN hubs r ON ((r.id = rm.hub_id)))   WHERE ((rm.learner_id = submissions.user_id) AND (r.mentor_id = auth.uid())))))` | — |
| `Service role full access on submissions` | ALL | service_role | PERMISSIVE | `true` | `true` |
| `Users can insert own submissions` | INSERT | authenticated | PERMISSIVE | — | `(auth.uid() = user_id)` |
| `Users can view own submissions` | SELECT | authenticated | PERMISSIVE | `(auth.uid() = user_id)` | — |

### `modules`

| Policy | Command | Roles | Action | USING | WITH CHECK |
|--------|---------|-------|--------|-------|------------|
| `Public can view modules` | SELECT | public | PERMISSIVE | `true` | — |

### `user_practice_progress`

| Policy | Command | Roles | Action | USING | WITH CHECK |
|--------|---------|-------|--------|-------|------------|
| `Users can insert own progress` | INSERT | public | PERMISSIVE | — | `(auth.uid() = user_id)` |
| `Users can select own progress` | SELECT | public | PERMISSIVE | `(auth.uid() = user_id)` | — |
| `Users can update own progress` | UPDATE | public | PERMISSIVE | `(auth.uid() = user_id)` | — |

### `module_reviews`

| Policy | Command | Roles | Action | USING | WITH CHECK |
|--------|---------|-------|--------|-------|------------|
| `Allow all on module_reviews` | ALL | public | PERMISSIVE | `true` | `true` |

### `hub_modules`

| Policy | Command | Roles | Action | USING | WITH CHECK |
|--------|---------|-------|--------|-------|------------|
| `Members view hub modules` | SELECT | public | PERMISSIVE | `(is_hub_member(hub_id, auth.uid()) OR is_hub_mentor(hub_id, auth.uid()) OR is_admin(auth.uid()))` | — |
| `Mentors manage hub modules` | ALL | public | PERMISSIVE | `(is_hub_mentor(hub_id, auth.uid()) OR is_admin(auth.uid()))` | `(is_hub_mentor(hub_id, auth.uid()) OR is_admin(auth.uid()))` |

### `user_streaks`

| Policy | Command | Roles | Action | USING | WITH CHECK |
|--------|---------|-------|--------|-------|------------|
| `Users can insert own streak` | INSERT | authenticated | PERMISSIVE | — | `(auth.uid() = user_id)` |
| `Users can update own streak` | UPDATE | authenticated | PERMISSIVE | `(auth.uid() = user_id)` | `(auth.uid() = user_id)` |
| `Users can view own streak` | SELECT | authenticated | PERMISSIVE | `(auth.uid() = user_id)` | — |

### `notifications`

| Policy | Command | Roles | Action | USING | WITH CHECK |
|--------|---------|-------|--------|-------|------------|
| `Authenticated users can insert notifications` | INSERT | authenticated | PERMISSIVE | — | `true` |
| `Users can update own notifications` | UPDATE | authenticated | PERMISSIVE | `(auth.uid() = user_id)` | `(auth.uid() = user_id)` |
| `Users can view own notifications` | SELECT | authenticated | PERMISSIVE | `(auth.uid() = user_id)` | — |

### `user_assessment_library`

| Policy | Command | Roles | Action | USING | WITH CHECK |
|--------|---------|-------|--------|-------|------------|
| `Users can manage own assessment library` | ALL | authenticated | PERMISSIVE | `(auth.uid() = user_id)` | `(auth.uid() = user_id)` |

### `mentor_profiles`

| Policy | Command | Roles | Action | USING | WITH CHECK |
|--------|---------|-------|--------|-------|------------|
| `Public can view mentor profiles` | SELECT | public | PERMISSIVE | `true` | — |
| `Users can insert own mentor profile` | INSERT | authenticated | PERMISSIVE | — | `(auth.uid() = user_id)` |
| `Users or admin can delete mentor profile` | DELETE | authenticated | PERMISSIVE | `((auth.uid() = user_id) OR (EXISTS ( SELECT 1    FROM profiles   WHERE ((profiles.user_id = auth.uid()) AND (profiles.user_role = 'admin'::text)))))` | — |
| `Users or admin can update mentor profile` | UPDATE | authenticated | PERMISSIVE | `((auth.uid() = user_id) OR (EXISTS ( SELECT 1    FROM profiles   WHERE ((profiles.user_id = auth.uid()) AND (profiles.user_role = 'admin'::text)))))` | `((auth.uid() = user_id) OR (EXISTS ( SELECT 1    FROM profiles   WHERE ((profiles.user_id = auth.uid()) AND (profiles.user_role = 'admin'::text)))))` |

### `assessments`

| Policy | Command | Roles | Action | USING | WITH CHECK |
|--------|---------|-------|--------|-------|------------|
| `Mentors and admins can insert assessments` | INSERT | authenticated | PERMISSIVE | — | `((auth.uid() = mentor_id) OR (EXISTS ( SELECT 1    FROM profiles   WHERE ((profiles.user_id = auth.uid()) AND (profiles.user_role = 'admin'::text)))))` |
| `Mentors can delete own assessments, admins can delete any` | DELETE | authenticated | PERMISSIVE | `((auth.uid() = mentor_id) OR (EXISTS ( SELECT 1    FROM profiles   WHERE ((profiles.user_id = auth.uid()) AND (profiles.user_role = 'admin'::text)))))` | — |
| `Mentors can update own assessments, admins can update any` | UPDATE | authenticated | PERMISSIVE | `((auth.uid() = mentor_id) OR (EXISTS ( SELECT 1    FROM profiles   WHERE ((profiles.user_id = auth.uid()) AND (profiles.user_role = 'admin'::text)))))` | `((auth.uid() = mentor_id) OR (EXISTS ( SELECT 1    FROM profiles   WHERE ((profiles.user_id = auth.uid()) AND (profiles.user_role = 'admin'::text)))))` |
| `Public and authenticated can read published assessments` | SELECT | public | PERMISSIVE | `((status = 'published'::text) OR (auth.uid() = mentor_id) OR (EXISTS ( SELECT 1    FROM profiles   WHERE ((profiles.user_id = auth.uid()) AND (profiles.user_role = 'admin'::text)))))` | — |

### `profiles`

| Policy | Command | Roles | Action | USING | WITH CHECK |
|--------|---------|-------|--------|-------|------------|
| `Public can view profiles` | SELECT | public | PERMISSIVE | `true` | — |
| `Users can insert own profile` | INSERT | authenticated | PERMISSIVE | — | `(auth.uid() = user_id)` |
| `Users can update own profile` | UPDATE | authenticated | PERMISSIVE | `(auth.uid() = user_id)` | `(auth.uid() = user_id)` |

### `activities`

| Policy | Command | Roles | Action | USING | WITH CHECK |
|--------|---------|-------|--------|-------|------------|
| `Authenticated users can delete activities` | DELETE | authenticated | PERMISSIVE | `true` | — |
| `Authenticated users can insert activities` | INSERT | authenticated | PERMISSIVE | — | `true` |
| `Authenticated users can update activities` | UPDATE | authenticated | PERMISSIVE | `true` | `true` |
| `Public can view activities` | SELECT | public | PERMISSIVE | `true` | — |

### `ai_audits`

| Policy | Command | Roles | Action | USING | WITH CHECK |
|--------|---------|-------|--------|-------|------------|
| `Users can view their submission audits` | SELECT | authenticated | PERMISSIVE | `(EXISTS ( SELECT 1    FROM submissions s   WHERE ((s.sub_id = ai_audits.sub_id) AND (s.user_id = auth.uid()))))` | — |

### `hubs`

| Policy | Command | Roles | Action | USING | WITH CHECK |
|--------|---------|-------|--------|-------|------------|
| `Enrolled learners view hubs` | SELECT | public | PERMISSIVE | `(is_hub_member(id, auth.uid()) OR (mentor_id = auth.uid()) OR is_admin(auth.uid()))` | — |
| `Lookup hub by join code` | SELECT | public | PERMISSIVE | `((auth.role() = 'authenticated'::text) AND (is_archived = false))` | — |
| `Mentors manage own hubs` | ALL | public | PERMISSIVE | `((mentor_id = auth.uid()) OR is_admin(auth.uid()))` | `((mentor_id = auth.uid()) OR is_admin(auth.uid()))` |

### `module_reports`

| Policy | Command | Roles | Action | USING | WITH CHECK |
|--------|---------|-------|--------|-------|------------|
| `Admins can delete reports` | DELETE | authenticated | PERMISSIVE | `(EXISTS ( SELECT 1    FROM profiles   WHERE ((profiles.user_id = auth.uid()) AND (profiles.user_role = 'admin'::text))))` | — |
| `Mentors can view reports for own modules` | SELECT | authenticated | PERMISSIVE | `(EXISTS ( SELECT 1    FROM modules m   WHERE ((m.mod_id = module_reports.mod_id) AND (m.mentor_id = auth.uid()))))` | — |
| `Users can submit reports` | INSERT | public | PERMISSIVE | — | `(((auth.uid() IS NOT NULL) AND ((user_id = auth.uid()) OR (user_id IS NULL))) OR ((auth.uid() IS NULL) AND (user_id IS NULL)))` |
| `Users can update own active report or admin update` | UPDATE | authenticated | PERMISSIVE | `(((auth.uid() = user_id) AND (report_status = ANY (ARRAY['pending'::text, 'investigating'::text]))) OR (EXISTS ( SELECT 1    FROM profiles   WHERE ((profiles.user_id = auth.uid()) AND (profiles.user_role = 'admin'::text)))))` | `(((auth.uid() = user_id) AND (report_status = ANY (ARRAY['pending'::text, 'investigating'::text]))) OR (EXISTS ( SELECT 1    FROM profiles   WHERE ((profiles.user_id = auth.uid()) AND (profiles.user_role = 'admin'::text)))))` |
| `Users or admins can view reports` | SELECT | authenticated | PERMISSIVE | `((auth.uid() = user_id) OR (EXISTS ( SELECT 1    FROM profiles   WHERE ((profiles.user_id = auth.uid()) AND (profiles.user_role = 'admin'::text)))))` | — |

### `hub_members`

| Policy | Command | Roles | Action | USING | WITH CHECK |
|--------|---------|-------|--------|-------|------------|
| `Learners can join hub` | INSERT | public | PERMISSIVE | — | `(learner_id = auth.uid())` |
| `Learners can leave hub` | DELETE | public | PERMISSIVE | `(learner_id = auth.uid())` | — |
| `Members view hub roster` | SELECT | public | PERMISSIVE | `((learner_id = auth.uid()) OR is_hub_mentor(hub_id, auth.uid()) OR is_admin(auth.uid()))` | — |
| `Mentors manage hub members` | ALL | public | PERMISSIVE | `(is_hub_mentor(hub_id, auth.uid()) OR is_admin(auth.uid()))` | `(is_hub_mentor(hub_id, auth.uid()) OR is_admin(auth.uid()))` |

### `hub_invitations`

| Policy | Command | Roles | Action | USING | WITH CHECK |
|--------|---------|-------|--------|-------|------------|
| `Learners view own hub invitations` | SELECT | public | PERMISSIVE | `(lower(invited_email) = lower((auth.jwt() ->> 'email'::text)))` | — |
| `Mentors manage hub invitations` | ALL | public | PERMISSIVE | `(is_hub_mentor(hub_id, auth.uid()) OR is_admin(auth.uid()))` | `(is_hub_mentor(hub_id, auth.uid()) OR is_admin(auth.uid()))` |

### `user_practice_saves`

| Policy | Command | Roles | Action | USING | WITH CHECK |
|--------|---------|-------|--------|-------|------------|
| `Users can delete own saves` | DELETE | public | PERMISSIVE | `((auth.uid() = user_id) OR (auth.uid() IS NOT NULL))` | — |
| `Users can insert own saves` | INSERT | public | PERMISSIVE | — | `((auth.uid() = user_id) OR (auth.uid() IS NOT NULL))` |
| `Users can select own saves` | SELECT | public | PERMISSIVE | `((auth.uid() = user_id) OR (auth.uid() IS NOT NULL))` | — |

### `user_wallets`

| Policy | Command | Roles | Action | USING | WITH CHECK |
|--------|---------|-------|--------|-------|------------|
| `Users read own wallet` | SELECT | public | PERMISSIVE | `(auth.uid() = user_id)` | — |

### `coin_transactions`

| Policy | Command | Roles | Action | USING | WITH CHECK |
|--------|---------|-------|--------|-------|------------|
| `Users read own coin transactions` | SELECT | public | PERMISSIVE | `(auth.uid() = user_id)` | — |

### `submission_feedback`

| Policy | Command | Roles | Action | USING | WITH CHECK |
|--------|---------|-------|--------|-------|------------|
| `Learners view own submission feedback` | SELECT | public | PERMISSIVE | `((learner_id = auth.uid()) AND (status = 'published'::text))` | — |
| `Mentors manage hub submission feedback` | ALL | public | PERMISSIVE | `(is_hub_mentor(hub_id, auth.uid()) OR is_admin(auth.uid()))` | `(is_hub_mentor(hub_id, auth.uid()) OR is_admin(auth.uid()))` |
| `Service role full access on submission_feedback` | ALL | service_role | PERMISSIVE | `true` | `true` |

### `assessment_challenges`

| Policy | Command | Roles | Action | USING | WITH CHECK |
|--------|---------|-------|--------|-------|------------|
| `Manage challenges for owned assessments` | ALL | authenticated | PERMISSIVE | `(EXISTS ( SELECT 1    FROM assessments a   WHERE ((a.id = assessment_challenges.assessment_id) AND ((a.mentor_id = auth.uid()) OR (EXISTS ( SELECT 1            FROM profiles p           WHERE ((p.user_id = auth.uid()) AND (p.user_role = 'admin'::text))))))))` | `(EXISTS ( SELECT 1    FROM assessments a   WHERE ((a.id = assessment_challenges.assessment_id) AND ((a.mentor_id = auth.uid()) OR (EXISTS ( SELECT 1            FROM profiles p           WHERE ((p.user_id = auth.uid()) AND (p.user_role = 'admin'::text))))))))` |
| `Read challenges for visible assessments` | SELECT | public | PERMISSIVE | `(EXISTS ( SELECT 1    FROM assessments a   WHERE ((a.id = assessment_challenges.assessment_id) AND ((a.status = 'published'::text) OR (a.mentor_id = auth.uid()) OR (EXISTS ( SELECT 1            FROM profiles p           WHERE ((p.user_id = auth.uid()) AND (p.user_role = 'admin'::text))))))))` | — |

### `assessment_reports`

| Policy | Command | Roles | Action | USING | WITH CHECK |
|--------|---------|-------|--------|-------|------------|
| `Admins can delete assessment reports` | DELETE | authenticated | PERMISSIVE | `(EXISTS ( SELECT 1    FROM profiles   WHERE ((profiles.user_id = auth.uid()) AND (profiles.user_role = 'admin'::text))))` | — |
| `Mentors can insert unlock requests for own assessments` | INSERT | authenticated | PERMISSIVE | — | `(EXISTS ( SELECT 1    FROM assessments a   WHERE ((a.id = assessment_reports.assessment_id) AND (a.mentor_id = auth.uid()))))` |
| `Mentors can view reports for own assessments` | SELECT | authenticated | PERMISSIVE | `(EXISTS ( SELECT 1    FROM assessments a   WHERE ((a.id = assessment_reports.assessment_id) AND (a.mentor_id = auth.uid()))))` | — |
| `Users can submit assessment reports` | INSERT | authenticated | PERMISSIVE | — | `(auth.uid() = user_id)` |
| `Users can update own active report or admin update` | UPDATE | authenticated | PERMISSIVE | `(((auth.uid() = user_id) AND (report_status = ANY (ARRAY['pending'::text, 'investigating'::text]))) OR (EXISTS ( SELECT 1    FROM profiles   WHERE ((profiles.user_id = auth.uid()) AND (profiles.user_role = 'admin'::text)))))` | `(((auth.uid() = user_id) AND (report_status = ANY (ARRAY['pending'::text, 'investigating'::text]))) OR (EXISTS ( SELECT 1    FROM profiles   WHERE ((profiles.user_id = auth.uid()) AND (profiles.user_role = 'admin'::text)))))` |
| `Users or admins can view assessment reports` | SELECT | authenticated | PERMISSIVE | `((auth.uid() = user_id) OR (EXISTS ( SELECT 1    FROM profiles   WHERE ((profiles.user_id = auth.uid()) AND (profiles.user_role = 'admin'::text)))))` | — |

