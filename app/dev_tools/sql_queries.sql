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