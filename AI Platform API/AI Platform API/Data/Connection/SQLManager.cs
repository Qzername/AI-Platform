using System.Data.Common;
using System.Data.SQLite;
using System.Reflection;

namespace UniversalTools
{
    public class SQLManager //ver. 2.0.1
    {
        string path;

        SQLiteConnection connection;

        public SQLManager(string path = "./Database/database.db") 
        { 
            this.path = "Data Source="+path;
            OpenConnection();
        }

        void OpenConnection()
        {
            connection = new SQLiteConnection(path);
            connection.Open();  
        }

        void CloseConnection() => connection.Close();

        /// <summary>
        /// Select multiple structs from database
        /// </summary>
        public T[] SelectMany<T>(string query) where T : struct
        {
            var command = new SQLiteCommand(query, connection);
            SQLiteDataReader reader = command.ExecuteReader();

            List<T> final = new List<T>();

            var columns = reader.GetColumnSchema();
            var fields = typeof(T).GetProperties();

            while (reader.Read())
            {
                object item = new T(); //it has to be this way because of field.SetValue

                for(int i = 0; i < reader.FieldCount; i++)
                {
                    DbColumn currentColumn = columns[i];

                    if (!fields.Any(x => x.Name == currentColumn.ColumnName))
                        continue;

                    PropertyInfo field = fields.Single(x=>x.Name == currentColumn.ColumnName);

                    var value = reader.GetValue(i);

                    if (value is DBNull)
                        continue;

                    field.SetValue(item, Convert.ChangeType(value, field.PropertyType));
                }

                final.Add((T)item);
            }

            return final.ToArray();
        }

        /// <summary>
        /// Select single struct from database
        /// </summary>
        public T SelectSingle<T>(string query) where T : struct
        {
            var objects = SelectMany<T>(query);

            if (objects.Length > 1)
                throw new Exception("Detected more than one value. Amount of values: " + objects.Length);

            return objects[0];
        }


        /// <summary>
        /// Select single value (such as string, int etc.) from database
        /// </summary>
        public T SelectSingleValue<T>(string query)
        {
            var command = new SQLiteCommand(query, connection);
            SQLiteDataReader reader = command.ExecuteReader();

            reader.Read();

            T t = (T)Convert.ChangeType(reader.GetValue(0), typeof(T));

            return t;
        }

        /// <summary>
        /// Execute query that doesn't return values
        /// </summary>
        public void ExecuteNonQuery(string command)
        {
            var SQLcommand = new SQLiteCommand(command, connection);
            SQLcommand.Prepare();
            SQLcommand.ExecuteNonQuery();
        }
    }
}
