FROM traffic_light_objects
LEFT OUTER JOIN regions AS regions_1 ON regions_1.id = traffic_light_objects.region_id
ORDER BY traffic_light_objects.id


SELECT
traffic_light_objects.region_id,
traffic_light_objects.name,
traffic_light_objects.district, traffic_light_objects.street,
traffic_light_objects.service_organization,
traffic_light_objects.description,
traffic_light_objects.ovim_passport_editing,
traffic_light_objects.stroykontrol_passport_editing,
traffic_light_objects.id, traffic_light_objects.created_at,
traffic_light_objects.updated_at,
regions_1.code,
regions_1.name AS name_1,
regions_1.id AS id_1,
regions_1.created_at AS created_at_1,
regions_1.updated_at AS updated_at_1
FROM traffic_light_objects
LEFT OUTER JOIN regions AS regions_1 ON regions_1.id = traffic_light_objects.region_id
ORDER BY traffic_light_objects.id


SELECT
traffic_light_objects.id AS tlo_id,

traffic_light_objects.name AS tlo_name,
passport_groups.id AS passport_group_id,
passport_groups.group_name AS passport_group_name,
passports.editing_now, passports.id AS
passport_id, passports.tlo_id AS tlo_id_1,
passports.started_editing_at, passports.finished_editing_at,
users.username AS username, users.id AS user_id
FROM traffic_light_objects, passport_groups, passports, users
WHERE traffic_light_objects.name = $1::VARCHAR
AND passport_groups.group_name_route = $2::VARCHAR
AND passports.tlo_id = traffic_light_objects.id
AND users.id = users.id
ORDER BY passports.finished_editing_at DESC
LIMIT $3::INTEGER ('413', <PassportGroupsRoutes.OVIM: 'ovim'>, 1)


SELECT
passports.user_id AS passport_user_id,
traffic_light_objects.id AS tlo_id,
traffic_light_objects.name AS tlo_name,
traffic_light_objects.street,
traffic_light_objects.service_organization,
regions.code AS region_code,
regions.name AS region_name,
passport_groups.id AS passport_group_id,
passport_groups.group_name AS passport_group_name,
passports.id AS passport_id,
passports.tlo_id AS tlo_id_1,
passports.data,
passports.commit_message,
passports.editing_now,
passports.started_editing_at,
passports.finished_editing_at,
users.username AS username
FROM passports, traffic_light_objects, regions, passport_groups, users
WHERE traffic_light_objects.name = $1::VARCHAR AND passport_groups.group_name_route = $2::VARCHAR AND passports.tlo_id = traffic_light_objects.id AND users.id = passports.user_id AND passports.group_id = passport_groups.id AND regions.id = traffic_light_objects.region_id ORDER BY passports.finished_editing_at DESC
LIMIT $3::INTEGER
