// your normal glue job imports
import com.amazonaws.services.glue.GlueContext
...

// import jdbc
import java.sql.{Connection, DriverManager}

object GlueApp {
  def main(sysArgs: Array[String]) {

    // your normal glue etl scripts
    val spark: SparkContext = new SparkContext()
    val glueContext: GlueContext = new GlueContext(spark)
    val args = GlueArgParser.getResolvedOptions(sysArgs, Seq("JOB_NAME").toArray)
    Job.init(args("JOB_NAME"), glueContext, args.asJava)
    ...


    //  postgresql connection sample
    var sql_connection: Connection = null
    Class.forName("org.postgresql.Driver")
    sql_connection = DriverManager.getConnection(
      "jdbc:postgresql://psql_url:5432/dbname", "username", "password")
    
    val prepare_statement = sql_connection.prepareStatement(s"some sql here ...")
    prepare_statement.executeUpdate()
    prepare_statement.close()


    Job.commit()
  }
}
