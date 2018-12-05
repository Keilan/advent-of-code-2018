object Polymer {
  def main(args: Array[String]): Unit = {
    var polymer = scala.io.StdIn.readLine()
    var reduced = ""
    println("Initial Reduction")
    while (polymer.length != reduced.length){
      reduced = polymer
      polymer = reduceChain(polymer)
    }
    println(polymer.length)

    var min = 50000
    for(letter <- 'a' to 'z'){
      var removed = polymer.filter(_.toLower != letter)
      var reduced = ""
      while (removed.length != reduced.length){
        reduced = removed
        removed = reduceChain(removed)
        if (removed.length < min){
          min = removed.length
        }
      }
      println(letter, removed.length)
    }
    println(min)
  }

  def reduceChain(polymer:String) : String = {
    val reduced = polymer.grouped(2).filter(x => x.length == 1 || x(0) == x(1) || x(0).toLower != x(1).toLower).mkString("")
    reduced(0) + reduced.substring(1).grouped(2).filter(x => x.length == 1 || x(0) == x(1) || x(0).toLower != x(1).toLower).mkString("")
  }
}