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

| Projects both in Sstubs and TravisTorrent |
| ----------------------------------------- |
| Graylog2.graylog2-server                  |
| apache.flink                              |
| apache.storm                              |
| aws.aws-sdk-java                          |
| brettwooldridge.HikariCP                  |
| brianfrankcooper.YCSB                     |
| checkstyle.checkstyle                     |
| code4craft.webmagic                       |
| deeplearning4j.deeplearning4j             |
| dropwizard.dropwizard                     |
| dropwizard.metrics                        |
| druid-io.druid                            |
| facebook.presto                           |
| google.auto                               |
| google.closure-compiler                   |
| google.guava                              |
| google.guice                              |
| iluwatar.java-design-patterns             |
| javaee-samples.javaee7-samples            |
| jhy.jsoup                                 |
| joelittlejohn.jsonschema2pojo             |
| junit-team.junit                          |
| knightliao.disconf                        |
| mybatis.mybatis-3                         |
| naver.pinpoint                            |
| perwendel.spark                           |
| roboguice.roboguice                       |
| springside.springside4                    |
| square.dagger                             |
| square.javapoet                           |
| square.okhttp                             |
| square.retrofit                           |
| thinkaurelius.titan                       |
| xetorthio.jedis                           |

## Phase 2
Filter the list according to the requirements: manual verification of the GitHub repo
- `.travis.yml` history
- Initial commit
- Current CI pipeline

<table class="tg">
<thead>
  <tr>
    <th class="tg-fymr">Projects both in Sstubs and TravisTorrent</th>
    <th class="tg-fymr">Project Age</th>
    <th class="tg-fymr">Travis History</th>
    <th class="tg-fymr">Still using Travis?</th>
  </tr>
</thead>
<tbody>
  <tr>
    <td class="tg-fymr">Graylog2.graylog2-server</td>
    <td class="tg-0pky">10 years</td>
    <td class="tg-0pky">8 years</td>
    <td class="tg-0pky">no</td>
  </tr>
  <tr>
    <td class="tg-fymr">apache.flink</td>
    <td class="tg-0pky">8 years</td>
    <td class="tg-0pky">7 years</td>
    <td class="tg-0pky">no</td>
  </tr>
  <tr>
    <td class="tg-fymr">apache.storm</td>
    <td class="tg-0pky">9 years</td>
    <td class="tg-0pky">5 years</td>
    <td class="tg-0pky">yes</td>
  </tr>
  <tr>
    <td class="tg-fymr">aws.aws-sdk-java</td>
    <td class="tg-0pky">11 years</td>
    <td class="tg-0pky">7 years</td>
    <td class="tg-0pky">yes</td>
  </tr>
  <tr>
    <td class="tg-fymr">brettwooldridge.HikariCP</td>
    <td class="tg-0pky">7 years<br></td>
    <td class="tg-0pky">7 years</td>
    <td class="tg-0pky">yes</td>
  </tr>
  <tr>
    <td class="tg-fymr">brianfrankcooper.YCSB</td>
    <td class="tg-0pky">11 years</td>
    <td class="tg-0pky">6 years</td>
    <td class="tg-0pky">yes</td>
  </tr>
  <tr>
    <td class="tg-fymr">checkstyle.checkstyle</td>
    <td class="tg-0pky">20 years</td>
    <td class="tg-0pky">7 years</td>
    <td class="tg-0pky">yes</td>
  </tr>
  <tr>
    <td class="tg-fymr">code4craft.webmagic</td>
    <td class="tg-0pky">8 years</td>
    <td class="tg-0pky">7 years</td>
    <td class="tg-0pky">yes</td>
  </tr>
  <tr>
    <td class="tg-fymr">deeplearning4j.deeplearning4j</td>
    <td class="tg-0pky">-</td>
    <td class="tg-0pky">-</td>
    <td class="tg-0pky">-</td>
  </tr>
  <tr>
    <td class="tg-fymr">dropwizard.dropwizard</td>
    <td class="tg-0pky">9 years</td>
    <td class="tg-0pky">7 years</td>
    <td class="tg-0pky">yes</td>
  </tr>
  <tr>
    <td class="tg-fymr">dropwizard.metrics</td>
    <td class="tg-0pky">9 years</td>
    <td class="tg-0pky">7 years</td>
    <td class="tg-0pky">yes</td>
  </tr>
  <tr>
    <td class="tg-fymr">druid-io.druid</td>
    <td class="tg-0pky">8 years</td>
    <td class="tg-0pky">6 years</td>
    <td class="tg-0pky">yes</td>
  </tr>
  <tr>
    <td class="tg-fymr">facebook.presto</td>
    <td class="tg-0pky">8 years</td>
    <td class="tg-0pky">7 years</td>
    <td class="tg-0pky">yes</td>
  </tr>
  <tr>
    <td class="tg-fymr">google.auto</td>
    <td class="tg-0pky">8 years</td>
    <td class="tg-0pky">7 years</td>
    <td class="tg-0pky">yes</td>
  </tr>
  <tr>
    <td class="tg-fymr">google.closure-compiler</td>
    <td class="tg-0pky">11 years</td>
    <td class="tg-0pky">6 years</td>
    <td class="tg-0pky">no</td>
  </tr>
  <tr>
    <td class="tg-fymr">google.guava</td>
    <td class="tg-0pky">11 years</td>
    <td class="tg-0pky">6 years</td>
    <td class="tg-0pky">yes</td>
  </tr>
  <tr>
    <td class="tg-fymr">google.guice</td>
    <td class="tg-0pky">15 years</td>
    <td class="tg-0pky">6 years</td>
    <td class="tg-0pky">yes</td>
  </tr>
  <tr>
    <td class="tg-fymr">iluwatar.java-design-patterns</td>
    <td class="tg-0pky">6 years</td>
    <td class="tg-0pky">6 years</td>
    <td class="tg-0pky">no</td>
  </tr>
  <tr>
    <td class="tg-fymr">javaee-samples.javaee7-samples</td>
    <td class="tg-0pky">7 year</td>
    <td class="tg-0pky">6 years</td>
    <td class="tg-0pky">yes</td>
  </tr>
  <tr>
    <td class="tg-fymr">jhy.jsoup</td>
    <td class="tg-0pky">10 years</td>
    <td class="tg-0pky">6 years</td>
    <td class="tg-0pky">no</td>
  </tr>
  <tr>
    <td class="tg-fymr">joelittlejohn.jsonschema2pojo</td>
    <td class="tg-0pky">10 years</td>
    <td class="tg-0pky">7 years</td>
    <td class="tg-0pky">yes</td>
  </tr>
  <tr>
    <td class="tg-fymr">junit-team.junit</td>
    <td class="tg-0pky">19 years</td>
    <td class="tg-0pky">7 years</td>
    <td class="tg-0pky">yes</td>
  </tr>
  <tr>
    <td class="tg-fymr">knightliao.disconf</td>
    <td class="tg-0pky">6 years</td>
    <td class="tg-0pky">6 years</td>
    <td class="tg-0pky">yes</td>
  </tr>
  <tr>
    <td class="tg-fymr">mybatis.mybatis-3</td>
    <td class="tg-0pky">11 years</td>
    <td class="tg-0pky">7 years</td>
    <td class="tg-0pky">no</td>
  </tr>
  <tr>
    <td class="tg-fymr">naver.pinpoint</td>
    <td class="tg-0pky">8 years</td>
    <td class="tg-0pky">5 years</td>
    <td class="tg-0pky">yes</td>
  </tr>
  <tr>
    <td class="tg-fymr">perwendel.spark</td>
    <td class="tg-0pky">10 years</td>
    <td class="tg-0pky">7 years</td>
    <td class="tg-0pky">yes</td>
  </tr>
  <tr>
    <td class="tg-fymr">roboguice.roboguice</td>
    <td class="tg-0pky">12 years</td>
    <td class="tg-0pky">8 years</td>
    <td class="tg-0pky">yes</td>
  </tr>
  <tr>
    <td class="tg-fymr">springside.springside4</td>
    <td class="tg-0pky">8 years</td>
    <td class="tg-0pky">7 years</td>
    <td class="tg-0pky">yes</td>
  </tr>
  <tr>
    <td class="tg-fymr">square.dagger</td>
    <td class="tg-0pky">9 years</td>
    <td class="tg-0pky">8 years</td>
    <td class="tg-0pky">yes</td>
  </tr>
  <tr>
    <td class="tg-fymr">square.javapoet</td>
    <td class="tg-0pky">8 years</td>
    <td class="tg-0pky">7 years</td>
    <td class="tg-0pky">yes</td>
  </tr>
  <tr>
    <td class="tg-fymr">square.okhttp</td>
    <td class="tg-0pky">9 years</td>
    <td class="tg-0pky">8 years</td>
    <td class="tg-0pky">no</td>
  </tr>
  <tr>
    <td class="tg-fymr">square.retrofit</td>
    <td class="tg-0pky">9 years</td>
    <td class="tg-0pky">8 years</td>
    <td class="tg-0pky">no</td>
  </tr>
  <tr>
    <td class="tg-fymr">thinkaurelius.titan</td>
    <td class="tg-0pky">9 years</td>
    <td class="tg-0pky">8 years</td>
    <td class="tg-0pky">no</td>
  </tr>
  <tr>
    <td class="tg-fymr">xetorthio.jedis</td>
    <td class="tg-0pky">10 years</td>
    <td class="tg-0pky">6 years</td>
    <td class="tg-0pky">no</td>
  </tr>
</tbody>
</table>

All projects except for deeplearning4j.deeplearning4j seem to be good candidates with rich Travis history. 

It is difficult to know if all commits are covered by CI. Once we narrow down the project list, we can: 
1. Create a smaller TravisTorrent dataset containing the projects we selected. 
2. Create a smaller Sstubs dataset containing commits related to the projects we selected
3. Verify if the sstubs commits are in the travis dataset. 
4. Create new table with sstubs commits that are also in travis torrent. 


**Step 1 -- Query TravisTorrent dataset to collect all commits from projects we selected**

`SELECT * from travistorrent-bq.data.2017_01_11 WHERE gh_project_name IN ('Graylog2/graylog2-server', 'apache/flink', 'apache/storm', 
'aws/aws-sdk-java', 'brettwooldridge/HikariCP', 'brianfrankcooper/YCSB', 'checkstyle/checkstyle', 'code4craft/webmagic', 'dropwizard/dropwizard', 'dropwizard/metrics', 'druid-io/druid', 'facebook/presto', 
'google/auto', 'google/closure-compiler', 'google/guava', 'google/guice', 'iluwatar/java-design-patterns', 
'javaee-samples/javaee7-samples', 'jhy/jsoup', 'joelittlejohn/jsonschema2pojo', 'junit-team/junit', 
'knightliao/disconf', 'mybatis/mybatis-3', 'naver/pinpoint', 'perwendel/spark', 'roboguice/roboguice', 
'springside/springside4', 'square/dagger', 'square/javapoet', 'square/okhttp', 'square/retrofit', 
'thinkaurelius/titan', 'xetorthio/jedis')`

Yields 62,985 Travis builds. 





Filter the list according to the requirements by querying the TravisTorrent dataset. 


