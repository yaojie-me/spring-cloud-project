package neo.matrix.provider.web;

import org.springframework.web.bind.annotation.GetMapping;
import org.springframework.web.bind.annotation.RequestParam;
import org.springframework.web.bind.annotation.RestController;

@RestController
public class HelloController {

    @GetMapping("/echo")
    public String echo(@RequestParam String param){
        return "received:" + param;
    }
}
