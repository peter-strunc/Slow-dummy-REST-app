
import com.fasterxml.jackson.databind.ObjectMapper
import org.apache.cxf.jaxrs.client.WebClient
import org.identityconnectors.framework.common.objects.Uid


log.info("Entering " + action + " Script");

WebClient webClient = client;
ObjectMapper mapper = new ObjectMapper();

String key;

switch (objectClass) {  
case "__ACCOUNT__":
  def user = [
    id:attributes.get("id")[0],
    username:attributes.get("username")[0]
  ]
  
  String payload = mapper.writeValueAsString(user);
  
  webClient.path("/user");
  webClient.post(payload);
  key = user['id'].toString();
  break

default:
  key = id;
}

return key;