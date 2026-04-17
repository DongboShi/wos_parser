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

-- item_doi
CREATE TABLE item_doi (
    uid VARCHAR(50),
    doi VARCHAR(255),
    INDEX idx_uid (uid),
    INDEX idx_doi (doi)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

INSERT IGNORE INTO item_doi (uid, doi)
SELECT uid, identifier_value AS doi FROM item_ids where identifier_type = 'doi';

UPDATE wos_xml.item_doi
SET doi = LOWER(doi)
WHERE doi IS NOT NULL
  AND doi <> LOWER(doi);
  

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

-- item_rp_cntry

CREATE TABLE item_rp_cntry (
    uid VARCHAR(50),
    country VARCHAR(255),
    INDEX idx_uid (uid),
    INDEX idx_country (country),
    UNIQUE INDEX idx_uid_country (uid, country)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

INSERT IGNORE INTO item_rp_cntry (uid, country)
SELECT uid, country FROM item_rp_addrs
WHERE country IS NOT NULL AND country IS NOT NULL AND country != '';


-- calculate highly cited papers

CREATE TABLE articles AS select distinct (a.uid), b.max_pubyear AS pubyear from item_doc_types_norm a join item_max_pubyear b on a.uid = b.uid where doctype_norm = 'Article';
CREATE INDEX idx_uid ON articles(uid);
ALTER TABLE articles ADD COLUMN subject VARCHAR(255);
CREATE INDEX idx_uid_ascatype ON item_subjects(uid, ascatype);
UPDATE articles a JOIN item_subjects s ON a.uid = s.uid SET a.subject = s.subject WHERE s.ascatype = 'traditional';
ALTER TABLE articles ADD COLUMN citation_count INT(10) DEFAULT 0;
UPDATE articles a JOIN cite_count c ON a.uid = c.cited_uid SET a.citation_count = c.citation_count;
ALTER TABLE articles ADD COLUMN top1 TINYINT(1);
ALTER TABLE articles 
ADD COLUMN threshold DECIMAL(10, 3)

UPDATE articles a
JOIN (
    SELECT 
        pubyear,
        subject,
        -- MySQL 计算 99th percentile
        PERCENTILE_CONT(0.99) WITHIN GROUP (ORDER BY citation_count) 
            OVER (PARTITION BY pubyear, subject) as threshold
    FROM articles
) t ON a.pubyear = t.pubyear 
   AND a.subject = t.subject
SET 
    a.threshold = t.threshold,
    a.top1 = CASE WHEN a.citation_count >= t.threshold THEN 1 ELSE 0 END;

ALTER TABLE articles ADD COLUMN ni82 TINYINT(1), ADD COLUMN top5 TINYINT(1), ADD COLUMN ns TINYINT(1);

-- modify item_micro_topics table 
CREATE TABLE item_micro_topics (
    uid VARCHAR(50),
    micro_topic_id VARCHAR(255),
    INDEX idx_uid (uid),
    INDEX idx_micro_topic_id (micro_topic_id),
    UNIQUE INDEX idx_uid_micro_topic_id (uid, micro_topic_id)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

INSERT IGNORE INTO item_micro_topics (uid, micro_topic_id)
SELECT uid, SUBSTRING_INDEX(TRIM(topic_micro), ' ', 1) AS micro_topic_id FROM item_topics;