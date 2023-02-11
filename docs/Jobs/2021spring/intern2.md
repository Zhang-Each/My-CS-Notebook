# 2021春招实习-设计模式
## 1. 单例模式
- 单例模式的**类的对象只允许一个实例存在**，比如服务器中的配置信息读取可以由单一对象完成
- 单例模式的实现主要通过以下两步：
   - 将该**类的构造方法定义为private**的，这样一来别的地方的代码就无法调用该类的构造方法来实例化该类的对象，只有通过该类提供的静态方法来访问该类产生的唯一一个对象
   - 在该类内**提供一个静态方法**，当我们调用这个方法时，如果类持有的引用不为空就返回这个引用，如果类保持的引用为空就创建该类的实例并将实例的引用赋予该类保持的引用



### 1.1 优缺点


- 优点
   - 在内存中只有一个对象，节省内存空间；
   - 避免频繁的创建销毁对象，可以提高性能；
   - 避免对共享资源的多重占用，简化访问；
   - 为整个系统提供一个全局访问点
- 缺点：
   - 不适用于变化频繁的对象；
   - 滥用单例将带来一些负面问题，如为了节省资源将数据库连接池对象设计为的单例类，可能会导致共享连接池对象的程序过多而出现连接池溢出；
   - 如果实例化的对象长时间不被利用，系统会认为该对象是垃圾而被回收，这可能会导致对象状态的丢失



### 实现方式1：饿汉式


- 一个简单的实现方式的代码如下：



```java
public class singleton1 {
    private static instance = new singleton1();
    private singleton1() {}
    public static singleton1 getInstance() {
        return instance;
    }
}
```


- 这种写法比较简单，在类装载的时候就完成实例化，没有达到Lazy Loading的效果。如果从始至终从未使用过这个实例，则会造成内存的浪费
   - 这种写法不用担心线程同步的问题



### 实现方式2：懒汉式


- 对饿汉式的实现方式做出了一定的改进，在需要的时候才对其进行实例化，问题就是不支持多线程的操作，否则会产生多个实例



```java
public class singleton1 {
    private static instance;
    private singleton1() {}
    public static singleton1 getInstance() {
        if (instance == null) {
            instance = new singleton1();
        }
        return instance;
    }
}
```


- 为了解决线程安全问题，可以进行双重加锁。在new之前看看互斥锁有没有上锁



## 2. 工厂模式


- 工厂模式可以分为简单工厂模式、工厂方法模式和抽象工厂模式
   - 在设计模式的分类中都属于**创建型模式**，三种模式依次从上到下逐渐抽象
   - 创建型模式对类的实例化这一过程进行了抽象，能够将软件模块中对象的创建和对象的使用分离
   - 对象的实例化过程是通过工厂实现的，用工厂代替new操作，使用工厂模式就可以



### 2.1 简单工厂模式


- 简单的工厂模式就是用factory提供的方法来代替**直接new一个新的product**，对外部封装了产品生产的过程，比如A接口派生出了B和C类，我们可以定义一个A工厂类来帮助我们产生新的B和C类
   - 简单工厂的模式不符合开闭原则



```java
abstract class A {
    A () { System.out.println("new A");}
}

class B extends A {
    B () { System.out.println("new B");}
}

class C extends A {
    C () { System.out.println("new C");}
}

class factory {
    B makeB () { return new B;}
    C makeC () { return new C;}
}
```


### 2.2 工厂方法模式


- 工厂方法模式包含 4 个角色（要素）：
   - Product：抽象产品，定义工厂方法所创建的对象的接口，也就是实际需要使用的对象的接口
   - ConcreteProduct：具体产品，具体的Product接口的实现对象
   - Factory：工厂接口，也可以叫 Creator(创建器)，声明工厂方法，通常返回一个 Product 类型的实例对象
   - ConcreteFactory：工厂实现，或者叫 ConcreteCreator(创建器对象)，覆盖 Factory 定义的工厂方法，返回具体的 Product 实例



```java
abstract class A {
    A () { System.out.println("new A");}
}

class B extends A {
    B () { System.out.println("new B");}
}

class C extends A {
    C () { System.out.println("new C");}
}

class AbstractFactory {
    A make() {}
}

class BFactory extends AbstractFactory {
    @override
    A make() { return new B; }
}
```


### 2.4 抽象工厂模式


- 可以创建多种类型的产品，抽象工厂模式通过在**AbstarctFactory中增加创建产品的接口**，并在具体子工厂中实现新加产品的创建，当然前提是子工厂支持生产该产品。否则继承的这个接口可以什么也不干


## 3. 建造者模式
### 3.1 简介

- 建造者模式使用多个简单的对象一步步构建一个复杂的对象，这种设计模式也是创建型模式，提供了一种创建对象的方式，一个Builder类会一步步构造最终的对象，并且是独立于其他对象的
   - 这种设计模式的目的是将复杂的构造函数与其表示相分离，使得同样的构建过程可以创建不同的表示
   - 主要解决了一些基本部件不变而其组合方式进场会变化的类的创建问题
      - 需要将变和不变分离开
      - Java中的StringBuilder就是使用建造者模式设计的
- 使用场景：生成的对象有复杂的内部结构，需要生成的对象的内部属性本身就互相依赖
### 3.2 建造者模式的实例

- 这是一个汉堡店套餐的类的设计模式，item是所有菜品的抽象，派生出了burger和drink等子类，然后meal类中有一个item的数组和若干方法，mealbuilder被用来创建不同的meal，具体的代码实现如下：
- 基本的食物类和“包装”类
```java
public interface Item {
   public String name();
   public Packing packing();
   public float price();    
}

public abstract class Burger implements Item {
   @Override
   public Packing packing() {
      return new Wrapper();
   }
 
   @Override
   public abstract float price();
}

public abstract class ColdDrink implements Item {
    @Override
    public Packing packing() {
       return new Bottle();
    }
 
    @Override
    public abstract float price();
}

public class VegBurger extends Burger {
   @Override
   public float price() {
      return 25.0f;
   }
 
   @Override
   public String name() {
      return "Veg Burger";
   }
}

public class Coke extends ColdDrink {
   @Override
   public float price() {
      return 30.0f;
   }
 
   @Override
   public String name() {
      return "Coke";
   }
}
```
```java
public interface Packing {
   public String pack();
}

public class Wrapper implements Packing {
 
   @Override
   public String pack() {
      return "Wrapper";
   }
}

public class Bottle implements Packing {
 
   @Override
   public String pack() {
      return "Bottle";
   }
}
```

- 构建一个meal类，可以表示不同的套餐
```java
public class Meal {
   private List<Item> items = new ArrayList<Item>();    
 
   public void addItem(Item item){
      items.add(item);
   }
 
   public float getCost(){
      float cost = 0.0f;
      for (Item item : items) {
         cost += item.price();
      }        
      return cost;
   }
 
   public void showItems(){
      for (Item item : items) {
         System.out.print("Item : "+item.name());
         System.out.print(", Packing : "+item.packing().pack());
         System.out.println(", Price : "+item.price());
      }        
   }    
}
```

- 最后构建一个meal的builder，用于构造不同内容的meal
```java
public class MealBuilder {
 
   public Meal prepareVegMeal (){
      Meal meal = new Meal();
      meal.addItem(new VegBurger());
      meal.addItem(new Coke());
      return meal;
   }   
 
   public Meal prepareNonVegMeal (){
      Meal meal = new Meal();
      meal.addItem(new ChickenBurger());
      meal.addItem(new Pepsi());
      return meal;
   }
}
```

- 这种设计模式下，虽然套餐有很多种，但是组成的内容无非是若干种汉堡和饮料，而套餐的形式固定了下来，当有套餐需要添加或者删除修改的时候，**只需要修改、添加builder类的构造方法**就可以了。





## 4. 原型模式
### 4.1 简介

- 原型模式Prototype Pattern是用于创建重复的对象，同时又能保证性能，也是创建型的设计模式，它提供了一种创建对象的方式。
   - 这种模式是实现了一个**原型接口**，该接口用于创建**当时对象的克隆**
- 原型模式允许用原型实例创建指定对象的种类，并且通过拷贝这些原型创建新的对象。
   - 实现原型模式的关键在于实现clone操作，使得对象变成可拷贝的
   - 原型模式同样用于隔离类对象的使用者和具体类型之间的耦合关系，同样要求这些易变类有稳定的结构
- 原型模式使得代码的性能提高，经常用于资源优化的场景
### 4.2 实例
- 在实现了shape接口和三种具体类之后可以创建一个ShapeCache来保存一系列的shape
```java
public class ShapeCache {
    
   private static Hashtable<String, Shape> shapeMap 
      = new Hashtable<String, Shape>();
 
   public static Shape getShape(String shapeId) {
      Shape cachedShape = shapeMap.get(shapeId);
      return (Shape) cachedShape.clone();
   }
    
   public static void loadCache() {
      Circle circle = new Circle();
      circle.setId("1");
      shapeMap.put(circle.getId(),circle);
      Square square = new Square();
      square.setId("2");
      shapeMap.put(square.getId(),square);
      Rectangle rectangle = new Rectangle();
      rectangle.setId("3");
      shapeMap.put(rectangle.getId(),rectangle);
   }
}

public class PrototypePatternDemo {
   public static void main(String[] args) {
      ShapeCache.loadCache(); // 先装载各类和对应的id
      Shape clonedShape = (Shape) ShapeCache.getShape("1");
      System.out.println("Shape : " + clonedShape.getType());        
      Shape clonedShape2 = (Shape) ShapeCache.getShape("2");
      System.out.println("Shape : " + clonedShape2.getType());        
      Shape clonedShape3 = (Shape) ShapeCache.getShape("3");
      System.out.println("Shape : " + clonedShape3.getType());        
   }
}
```


## 5. 适配器模式
### 5.1 简介

- 适配器模式是作为**两个不兼容的接口之间的桥梁**，这是一种结构型模式，结合了两个独立接口的功能
   - 目的是将一个类的接口转换成客户希望的另外一个接口，适配器模式使得原来由于接口不兼容而不能工作的类可以一起工作
   - 主要的实现方式是继承或者依赖
- 一个接口可能有多个实现方法，但是不需要继承一个接口全部的实现所有的方法，而是用一个抽象类继承接口，然后再选择性地继承和覆盖其中一些方法就可以
- 一个很经典的例子就是Java中中的JDBC就是一个Java和数据库的适配器
### 5.2 实例
- 上面这个就是一个适配器模式的设计，为了使AudioPlayer可以使用advance中的功能，可以设计一个adapter类供player使用
```java
public class MediaAdapter implements MediaPlayer {
 
   AdvancedMediaPlayer advancedMusicPlayer;
 
   public MediaAdapter(String audioType){
      if(audioType.equalsIgnoreCase("vlc") ){
         advancedMusicPlayer = new VlcPlayer();       
      } else if (audioType.equalsIgnoreCase("mp4")){
         advancedMusicPlayer = new Mp4Player();
      }  
   }
 
   @Override
   public void play(String audioType, String fileName) {
      if(audioType.equalsIgnoreCase("vlc")){
         advancedMusicPlayer.playVlc(fileName);
      }else if(audioType.equalsIgnoreCase("mp4")){
         advancedMusicPlayer.playMp4(fileName);
      }
   }
}

public class AudioPlayer implements MediaPlayer {
   MediaAdapter mediaAdapter; 
 
   @Override
   public void play(String audioType, String fileName) {    
 
      //播放 mp3 音乐文件的内置支持
      if(audioType.equalsIgnoreCase("mp3")){
         System.out.println("Playing mp3 file. Name: "+ fileName);         
      } 
      //mediaAdapter 提供了播放其他文件格式的支持
      else if(audioType.equalsIgnoreCase("vlc") 
         || audioType.equalsIgnoreCase("mp4")){
         mediaAdapter = new MediaAdapter(audioType);
         mediaAdapter.play(audioType, fileName);
      }
      else{
         System.out.println("Invalid media. "+
            audioType + " format not supported");
      }
   }   
}
```


## 6. 组合模式

- 又叫整体部分模式，其实就是类之间的组合，将一个类拆分成若干更具体的类的组合然后分别实现，按照一定的层次组合起来，这种设计模式属于结构型模式，说是模式其实是非常常用的模式。
- 具体的就不用多说了



## 7. 装饰器模式

- 装饰器模式允许像一个现有的对象添加新的功能同时又不改变其原本的结构，这种设计模式是结构型模式，其实就是对现有的类进行一次包装。
- 装饰类和被装饰类都可以独立扩展，不会相互耦合，装饰器模式比生成一个子类更为灵活。
   - 具体步骤是先抽象出总的装饰器类，再继承出一个具体的装饰器
```java
public abstract class ShapeDecorator implements Shape {
   protected Shape decoratedShape;
 
   public ShapeDecorator(Shape decoratedShape){
      this.decoratedShape = decoratedShape;
   }
 
   public void draw(){
      decoratedShape.draw();
   }  
}

public class RedShapeDecorator extends ShapeDecorator {
 
   public RedShapeDecorator(Shape decoratedShape) {
      super(decoratedShape);     
   }
 
   @Override
   public void draw() {
      decoratedShape.draw();         
      setRedBorder(decoratedShape);
   }
 
   private void setRedBorder(Shape decoratedShape){
      System.out.println("Border Color: Red");
   }
}
```




## 8. 观察者模式

- 假设A对B的某个属性的变化非常敏感，当B的这个属性发生变化的时候A也需要相应地作出一些反映，这个时候就需要使用观察者模式，这里A就是观察者，B就是被观察者，当B中的属性发生变化的时候会立即通知与B关联的A对象。
- 实现的关键在于在抽象类里面存放一系列的观察者。
- 举例：使用三个类Subject、Observer和Client来实现观察者模式，其中Subject对象带有绑定观察者到client对象和从client对象中解绑观察者的方法，具体的代码如下：
- Subject类有一个状态state，同时有一系列的观察者
```java
public class Subject {
   private List<Observer> observers 
      = new ArrayList<Observer>();
   private int state;
 
   public int getState() {
      return state;
   }
 
   public void setState(int state) {
      this.state = state;
      notifyAllObservers();
   }
 
   public void attach(Observer observer){
      observers.add(observer);      
   }
 
   public void notifyAllObservers(){
      for (Observer observer : observers) {
         observer.update();
      }
   }  
}
```

- 然后实现一个抽象类Observer，对Subject类进行一步封装
```java
public abstract class Observer {
   protected Subject subject;
   public abstract void update();
}
```

- 然后实现具体的Observer类，
```java
public class BinaryObserver extends Observer{
 
   public BinaryObserver(Subject subject){
      this.subject = subject;
      this.subject.attach(this);
   }
 
   @Override
   public void update() {
      System.out.println( "Binary String: " 
      + Integer.toBinaryString( subject.getState() ) ); 
   }
}
```
