#!/usr/bin/env scala

object Fabric {
    case class Claim(id: Int, left: Int, top: Int, width: Int, height: Int) {
        def columns = top until top + height
        def rows = left until left + width
        def eachSquare[A](f: (Int, Int) => A): Vector[A] = {
            for (i <- columns; j <- rows) yield f(i,j)
        }.toVector
    }

    def main(args: Array[String]): Unit = {
        // Setup Map
        val fabric = Array.ofDim[Int](1050,1050)

        val input = scala.io.Source.fromInputStream(System.in)
            .getLines
            .map(parseClaim)
            .toVector

        // Loop through input to build fabric array
        for (claim <- input) {
            claim.eachSquare{ (i,j) =>
                fabric(i)(j) = if (fabric(i)(j) != 0) -1 else claim.id
            }
        }

        // Loop through again to find input that doesn't conflict
        for (claim <- input) {
            val conflict = claim.eachSquare((i, j) => fabric(i)(j)).exists(_ == -1)
            if (!conflict) {
                println(s"No conflict in ${claim.id}")
            }
        }

        val overlap = fabric.map(row => row.count(_ == -1)).sum
        println(s"There are $overlap square inches of overlap")
    }

    def parseClaim(claim:String) : Claim = {
        val data = claim.split("\\D+").filter(_.nonEmpty)
        Claim(data(0).toInt, data(1).toInt, data(2).toInt, data(3).toInt, data(4).toInt)
    }
}
