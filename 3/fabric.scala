object Fabric {
    def main(args: Array[String]): Unit = {
        // Setup Map
        var fabric = Array.ofDim[Int](1050,1050)

        var input = List[String]()
        var line = ""
        while ({line = scala.io.StdIn.readLine(); line != null}) {
            input = line :: input
        }

        // Loop through input to build fabric array
        for (line <- input.reverse) {
            val (id, left, top, width, height) = parse_claim(line)

            for (i <- top to top+height-1; j <- left to left+width-1){
                if (fabric(i)(j) != 0){
                    fabric(i)(j) = -1
                }
                else {
                    fabric(i)(j) = id
                }
            }
        }

        // Loop through again to find input that doesn't conflict
        for (line <- input.reverse) {
            val (id, left, top, width, height) = parse_claim(line)

            var conflict = false
            for (i <- top to top+height-1; j <- left to left+width-1){
                if (fabric(i)(j) == -1){
                    conflict = true
                }
            }
            if (!conflict) {
                println(s"No conflict in $id")
            }
        }

        var overlap = 0
        for (row <- fabric){
            overlap += row.count(_ == -1)
        }
        println(s"There are $overlap square inches of overlap")
    }

    def parse_claim(claim:String) : (Int, Int, Int, Int, Int) = {
        val data = claim.split("\\D+").filter(_.nonEmpty)
        (data(0).toInt, data(1).toInt, data(2).toInt, data(3).toInt, data(4).toInt)
    }
}
