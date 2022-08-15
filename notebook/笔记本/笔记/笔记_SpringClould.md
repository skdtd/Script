<!-- URL -->
[源码]: https://github.com/spring-projects "Spring 项目源码"
[版本对应关系]: https://spring.io/projects/spring-cloud#overview "Spring Boot和Cloud的对应关系"
[技术选型]: https://start.spring.io/actuator/info "各版本对应关系"
[推荐版本]: https://docs.spring.io/spring-cloud/docs/current/reference/html/ "Spring Cloud对应的Boot"
[archetype-catalog.xml]: https://repo1.maven.org/maven2/archetype-catalog.xml "archetype-catalog.xml"

>  Spring Cloud 链接
>> [源码][源码]<br/>
>> [版本对应关系][版本对应关系]<br/>
>> [技术选型][技术选型]<br/>
>> [最新版Spring Cloud对应Boot版本][推荐版本]<br/>
>
>  IDEA 创建 MAVEN 项目卡在 Generating project in Batch mode
>> 下载[archetype-catalog.xml][archetype-catalog.xml]到
>> ~/.m2/repository/org/apache/maven/archetype/archetype-catalog/x.x.x/
>> 在idea工程目录中取得运行命令,在末尾加上以下参数
>>
>> ```bash
>> -X # debug模式
>> -DarchetypeCatalog=local #本地模式
>> ```