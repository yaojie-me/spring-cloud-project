package neo.matrix.consumer.client;

import org.springframework.cloud.openfeign.FeignClient;
import org.springframework.web.bind.annotation.PathVariable;
import org.springframework.web.bind.annotation.RequestMapping;
import org.springframework.web.bind.annotation.RequestMethod;

@FeignClient("feign-service")
@RequestMapping("/feign-service")
public interface FeignServiceClient {

    @RequestMapping(value = "/instance/{serviceId}",method = RequestMethod.GET)
    Object getInstanceByServiceId(@PathVariable("serviceId") String serviceId);
}
