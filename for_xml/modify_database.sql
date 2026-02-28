CREATE TABLE citations AS SELECT uid, cited_uid FROM item_references WHERE cited_uid LIKE 'WOS:%';

CREATE INDEX idx_citations_cited_uid ON citations(cited_uid); 
CREATE INDEX idx_citations_uid ON citations(uid); 
CREATE INDEX idx_citations_uid_cited_uid ON citations(uid, cited_uid);
DELETE FROM citations WHERE cited_uid LIKE '%.%';

CREATE TABLE IF NOT EXISTS tmp (
    uid VARCHAR(50),
    cited_uid VARCHAR(50),
    INDEX idx_uid (uid),
    INDEX idx_cited_uid (cited_uid),
    UNIQUE INDEX idx_uid_cited_uid (uid, cited_uid)
);

INSERT INTO tmp (uid, cited_uid) SELECT uid, cited_uid FROM citations GROUP BY uid, cited_uid;
INSERT IGNORE INTO tmp SELECT CONCAT('WOS:', ut), CONCAT('WOS:', utcited) FROM thomson.cite_to_cite;
RENAME TABLE tmp TO citation_merge;

CREATE TABLE cite_count AS SELECT cited_uid, COUNT(uid) AS citation_count FROM citation_merge GROUP BY cited_uid;
CREATE INDEX idx_cite_count_cited_uid ON cite_count(cited_uid);

CREATE TABLE item_max_pubyear (
    uid VARCHAR(50),
    max_pubyear SMALLINT,
    UNIQUE INDEX idx_uid (uid),
    INDEX idx_max_pubyear (max_pubyear)
);

INSERT IGNORE INTO item_max_pubyear SELECT uid, max(pubyear) FROM item GROUP BY uid;

-- thomson
USE thomson;
CREATE TABLE item_pubyear (
    uid VARCHAR(50),
    pubyear SMALLINT,
    INDEX idx_uid_pubyear (uid,pubyear));

INSERT INTO item_pubyear select CONCAT('WOS:', ut) AS uid, py AS pubyear from thomson.sourceitems as a join thomson.sourceissues AS b on a.ui = b.ui;
CREATE TABLE item_max_pubyear (
    uid VARCHAR(50),
    max_pubyear SMALLINT,
    UNIQUE INDEX idx_uid (uid),
    INDEX idx_max_pubyear (max_pubyear)
);
INSERT IGNORE INTO item_max_pubyear SELECT uid, max(pubyear) FROM item_pubyear GROUP BY uid;

INSERT IGNORE INTO wos_xml.item_max_pubyear SELECT uid, max_pubyear FROM thomson.item_max_pubyear;

USE wos_xml;

CREATE TABLE citation_merge_year AS SELECT cm.uid, cm.cited_uid, ip.max_pubyear AS citing_year
FROM citation_merge cm
JOIN item_max_pubyear ip ON cm.uid = ip.uid;

CREATE INDEX idx_citation_merge_year_cited_uid ON citation_merge_year(cited_uid, citing_year);

CREATE TABLE cite_count_year AS SELECT cited_uid, citing_year, COUNT(uid) AS citation_count FROM citation_merge_year GROUP BY cited_uid, citing_year;
