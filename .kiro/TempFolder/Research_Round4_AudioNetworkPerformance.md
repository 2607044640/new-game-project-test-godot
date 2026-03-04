# 研究轮次 4：音频、网络和性能优化

## 音频系统

### 关键发现

1. **AudioStreamPlayer 类型**
- AudioStreamPlayer - 全局音频（UI、BGM）
- AudioStreamPlayer2D - 2D 位置音频
- AudioStreamPlayer3D - 3D 位置音频

2. **播放音频**
```csharp
public partial class AudioManager : Node
{
    [Export] public AudioStream BackgroundMusic;
    [Export] public AudioStream JumpSound;
    
    private AudioStreamPlayer _musicPlayer;
    private AudioStreamPlayer _sfxPlayer;
    
    public override void _Ready()
    {
        // BGM 播放器
        _musicPlayer = new AudioStreamPlayer();
        _musicPlayer.Stream = BackgroundMusic;
        _musicPlayer.Autoplay = true;
        _musicPlayer.Bus = "Music";
        AddChild(_musicPlayer);
        
        // SFX 播放器
        _sfxPlayer = new AudioStreamPlayer();
        _sfxPlayer.Bus = "SFX";
        AddChild(_sfxPlayer);
    }
    
    public void PlaySound(AudioStream sound)
    {
        _sfxPlayer.Stream = sound;
        _sfxPlayer.Play();
    }
}
```

3. **Audio Bus 系统**
```csharp
// 设置音量（0.0 到 1.0）
float volume = 0.8f;
int busIndex = AudioServer.GetBusIndex("Master");
AudioServer.SetBusVolumeDb(busIndex, Mathf.LinearToDb(volume));

// 静音
AudioServer.SetBusMute(busIndex, true);
```


4. **音频池（避免重复创建）**
```csharp
public partial class AudioPool : Node
{
    [Export] public int PoolSize = 10;
    private List<AudioStreamPlayer> _pool = new();
    
    public override void _Ready()
    {
        for (int i = 0; i < PoolSize; i++)
        {
            var player = new AudioStreamPlayer();
            AddChild(player);
            _pool.Add(player);
        }
    }
    
    public void PlaySound(AudioStream sound)
    {
        foreach (var player in _pool)
        {
            if (!player.Playing)
            {
                player.Stream = sound;
                player.Play();
                return;
            }
        }
    }
}
```

## 网络多人游戏

### 关键发现

1. **RPC（远程过程调用）**
```csharp
public partial class Player : CharacterBody2D
{
    [Rpc(MultiplayerApi.RpcMode.AnyPeer)]
    public void TakeDamage(int amount)
    {
        Health -= amount;
        GD.Print($"受到 {amount} 伤害");
    }
    
    public void Attack()
    {
        // 调用所有客户端的方法
        Rpc(MethodName.TakeDamage, 10);
    }
}
```

2. **MultiplayerSynchronizer**
```csharp
// 自动同步属性
public partial class NetworkedPlayer : CharacterBody2D
{
    [Export] public int Health { get; set; } = 100;
    
    public override void _Ready()
    {
        var sync = new MultiplayerSynchronizer();
        sync.RootPath = GetPath();
        AddChild(sync);
        
        // 配置同步属性
        sync.ReplicationConfig = new SceneReplicationConfig();
        sync.ReplicationConfig.AddProperty(".:Health");
        sync.ReplicationConfig.AddProperty(".:Position");
    }
}
```

## 性能优化

### 关键发现

1. **使用 Profiler**
- Debugger > Profiler 查看性能瓶颈
- C# 脚本需要使用 JetBrains Rider + dotTrace

2. **缓存节点引用**
```csharp
// 差
public override void _Process(double delta)
{
    GetNode<Sprite2D>("Sprite").Position += Vector2.Right;
}

// 好
private Sprite2D _sprite;
public override void _Ready()
{
    _sprite = GetNode<Sprite2D>("Sprite");
}
public override void _Process(double delta)
{
    _sprite.Position += Vector2.Right;
}
```

3. **减少 Marshalling 开销**
```csharp
// 差 - 每次都调用 Godot API
for (int i = 0; i < 1000; i++)
{
    Position += Vector2.Right;
}

// 好 - 缓存到本地变量
Vector2 pos = Position;
for (int i = 0; i < 1000; i++)
{
    pos += Vector2.Right;
}
Position = pos;
```

## 需要添加的内容
1. 完整音频管理系统
2. RPC 和网络同步
3. 性能优化技巧
