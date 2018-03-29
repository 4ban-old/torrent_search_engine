BEGIN;

INSERT INTO domains (domain, specific) VALUES ('rutracker.org', '{"Nibbler": {"xpath_to_source": "(//div[@class=\\"post_body\\"])[1]"}}');
INSERT INTO domains (domain, specific) VALUES ('nnm-club.me', '{"Nibbler": {"xpath_to_source": "//td[@class=\\"row1\\"])[2]"}}');
INSERT INTO domains (domain, specific) VALUES ('tapochek.net', '{"Nibbler": {"xpath_to_source": "(//div[@class=\\"post_body\\"])[1]"}}');

COMMIT;