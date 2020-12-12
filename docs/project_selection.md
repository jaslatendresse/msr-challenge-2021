# Project Selection

We want to select 10-30 sizable projects that are fairly young (for mature CI usage) and that have been using CI from the beginning to ensure every commits are covered by CI. 

## Requirements 
- NLOC >= 5,000
- Use of Travis CI
- Have a baseline of less than 6 years of CI use
    - Have been using CI from the beginning of the project
- The project has at least one of each of the 16 bugType template. 

## Methodology
**Information on data format** -- https://travistorrent.testroots.org/page_dataformat/

### Phase 1
**Select projects that are in both datasets (Sstubs and TravisTorrent)**
1. Query the TravisTorrent dataset to obtain all the project names and output to JSON (SELECT * is too big and right now we only want to select the project names) from GoogleCloud Platform (BigQuery) 
2. Dump the JSON data into my existing SQLITe database (sstubs.db). 
3. Query the tables to select projects that are in both tables. 

`SELECT DISTINCT projectName FROM commits WHERE projectName IN(SELECT * from names)`

**Output** -- 34 results

| Projects both in Sstubs and TravisTorrent   |
| ------------------------------------------- |
| Graylog2.graylog2-server                    |
| apache.flink                                |
| apache.storm                                |
| aws.aws-sdk-java                            |
| brettwooldridge.HikariCP                    |
| brianfrankcooper.YCSB                       |
| checkstyle.checkstyle                       |
| code4craft.webmagic                         |
| deeplearning4j.deeplearning4j               |
| dropwizard.dropwizard                       |
| dropwizard.metrics                          |
| druid-io.druid                              |
| facebook.presto                             |
| google.auto                                 |
| google.closure-compiler                     |
| google.guava                                |
| google.guice                                |
| iluwatar.java-design-patterns               |
| javaee-samples.javaee7-samples              |
| jhy.jsoup                                   |
| joelittlejohn.jsonschema2pojo               |
| junit-team.junit                            |
| knightliao.disconf                          |
| mybatis.mybatis-3                           |
| naver.pinpoint                              |
| perwendel.spark                             |
| roboguice.roboguice                         |
| springside.springside4                      |
| square.dagger                               |
| square.javapoet                             |
| square.okhttp                               |
| square.retrofit                             |
| thinkaurelius.titan                         |
| xetorthio.jedis                             |

## Phase 2
Filter the list according to the requirements by querying the TravisTorrent dataset. 


