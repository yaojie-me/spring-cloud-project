package neo.matrix.consumer.web;

import org.springframework.web.bind.annotation.GetMapping;
import org.springframework.web.bind.annotation.RequestParam;
import org.springframework.web.bind.annotation.RestController;

@RestController
public class HelloController {

    @GetMapping("/consume")
    public String consume(@RequestParam String param){
        return "consume:" + param;
    }
}
